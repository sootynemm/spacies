// Standard Library Imports
use std::error::Error;
use std::io::{self, Write};
use std::sync::mpsc; // Channel support
use std::thread; // Thread support
use std::time::{Duration, Instant};

// External crate imports
use crossterm::cursor::{Hide, Show};
use crossterm::event::{self, Event, KeyCode};
use crossterm::execute;
use crossterm::terminal::{self, EnterAlternateScreen, LeaveAlternateScreen};
use rusty_audio::Audio;

// Local module imports
use spacies::frames::{new_frame, Drawable};
use spacies::player::Player;
// use spacies::frames::Frame; // delete later if unused
use spacies::render::render;
use spacies::spacies::Spacies;

fn main() -> Result<(), Box<dyn Error>> {
    let mut audio = Audio::new();
    audio.add("explosion", "explosion.wav");
    audio.add("victory", "victory_jingle.wav");
    audio.add("lose", "losing_retro.wav");
    audio.add("budge", "budge.wav");
    audio.add("laser_fire", "laser_fire.wav");
    audio.add("startup_theme", "startup_theme.wav");
    audio.add("close_encounters", "close_encounters.wav");
    audio.play("startup_theme");

    // Create terminal
    let mut stdout = io::stdout();
    terminal::enable_raw_mode()?;
    execute!(stdout, EnterAlternateScreen, Hide)?; // Modify this line CGPT

    // render loop in separate thread
    let (render_tx, render_rx) = mpsc::channel();
    let render_handle = thread::spawn(move || {
        let mut last_frame = new_frame();
        let mut stdout = io::stdout();
        render(&mut stdout, &last_frame, &last_frame, true);
        loop {
            let curr_frame = match render_rx.recv() {
                Ok(x) => x,
                Err(_) => break,
            };
            render(&mut stdout, &last_frame, &curr_frame, false);
            last_frame = curr_frame;
        }
    });

    // Main Game Loop
    let mut player = Player::new();
    let mut instant = Instant::now();
    let mut spacies = Spacies::new();
    'gameloop: loop {
        // Per-frame init
        let delta = instant.elapsed();
        instant = Instant::now();
        let mut curr_frame = new_frame();

        // input
        while event::poll(Duration::default())? {
            if let Event::Key(key_event) = event::read()? {
                match key_event.code {
                    KeyCode::Left => player.move_left(),
                    KeyCode::Right => player.move_right(),
                    KeyCode::Char(' ') | KeyCode::Enter => {
                        if player.shoot() {
                            audio.play("laser_fire");
                        }
                    }
                    KeyCode::Esc | KeyCode::Char('q') => {
                        audio.play("lose");
                        break 'gameloop;
                    }
                    _ => {}
                }
            }
        }

        // Updates
        player.update(delta);
        if spacies.update(delta) {
            audio.play("budge");
        }
        if player.detect_hits(&mut spacies) {
            audio.play("explosion");
        }

        // Draw and render section
        let drawables: Vec<&dyn Drawable> = vec![&player, &spacies];
        for drawable in drawables {
            drawable.draw(&mut curr_frame);
        }
        let _ = render_tx.send(curr_frame);
        thread::sleep(Duration::from_millis(1));

        // Win or lose section
        if spacies.all_killed() {
            audio.play("victory");
            break 'gameloop;
        }
        if spacies.reached_bottom() {
            audio.play("lose");
            break 'gameloop;
        }
    }

    // Cleanup
    drop(render_tx);
    render_handle.join().unwrap();
    audio.wait();
    execute!(stdout, Show, LeaveAlternateScreen)?; // Modify this line CGPT
    terminal::disable_raw_mode()?;
    Ok(())
}
