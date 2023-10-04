use std::time::Duration;

use crate::{
    frames::{Drawable, Frame},
    shot::Shot,
    spacies::Spacies,
    NUM_COLS, NUM_ROWS,
};

pub struct Player {
    x: usize,
    y: usize,
    shots: Vec<Shot>,
}

impl Player {
    pub fn new() -> Self {
        Self {
            x: NUM_COLS / 2,
            y: NUM_ROWS - 1,
            shots: Vec::new(),
        }
    }
    pub fn move_left(&mut self) {
        if self.x > 0 {
            self.x -= 1;
        }
    }
    pub fn move_right(&mut self) {
        if self.x < NUM_COLS - 1 {
            self.x += 1;
        }
    }
    pub fn shoot(&mut self) -> bool {
        if self.shots.len() < 3 {
            self.shots.push(Shot::new(self.x, self.y - 1));
            true
        } else {
            false
        }
    }
    pub fn update(&mut self, delta: Duration) {
        for shot in self.shots.iter_mut() {
            shot.update(delta);
        }
        self.shots.retain(|shot| !shot.dead());
    }
    pub fn detect_hits(&mut self, spacies: &mut Spacies) -> bool {
        let mut hit_something = false; // Corrected variable name
        for shot in self.shots.iter_mut() {
            if !shot.exploding {
                if spacies.kill_spacie_at(shot.x, shot.y) {
                    hit_something = true; // Consistent with above declaration
                    shot.explode();
                }
            }
        }
        hit_something // Moved out of the loop to correctly return the final status
    }
}

impl Drawable for Player {
    fn draw(&self, frame: &mut Frame) {
        frame[self.x][self.y] = "🚀";
        for shot in self.shots.iter() {
            shot.draw(frame);
        }
    }
}
