use std::{cmp::max, time::Duration};

use rusty_time::timer::Timer;

use crate::{
    frames::{Drawable, Frame},
    NUM_COLS, NUM_ROWS,
};

pub struct Spacie {
    pub x: usize,
    pub y: usize,
}

pub struct Spacies {
    pub fleet: Vec<Spacie>,
    move_timer: Timer,
    direction: i32,
}

impl Spacies {
    pub fn new() -> Self {
        let mut fleet = Vec::new();
        for x in 0..NUM_COLS {
            for y in 0..NUM_ROWS {
                if (x > 1)
                    && (x < NUM_COLS - 2)
                    && (y > 0)
                    && (y < 9) // or some value based off NUM_ROWS
                    && (x % 2 == 0)
                    && (y % 2 == 0)
                {
                    fleet.push(Spacie { x, y });
                }
            }
        }
        Self {
            fleet,
            move_timer: Timer::from_millis(2000),
            direction: 1,
        }
    }
    pub fn update(&mut self, delta: Duration) -> bool {
        self.move_timer.update(delta);
        if self.move_timer.ready {
            self.move_timer.reset();
            let mut downwards = false;
            if self.direction == -1 {
                let min_x = self.fleet.iter().map(|spacie| spacie.x).min().unwrap_or(0);
                if min_x == 0 {
                    self.direction = 1;
                    downwards = true;
                }
            } else {
                let max_x = self.fleet.iter().map(|spacie| spacie.x).max().unwrap_or(0);
                if max_x == NUM_COLS - 1 {
                    self.direction = -1;
                    downwards = true;
                }
            }
            if downwards {
                let new_duration = max(self.move_timer.duration.as_millis() - 250, 250);
                self.move_timer = Timer::from_millis(new_duration as u64);
                for spacie in self.fleet.iter_mut() {
                    spacie.y += 1;
                }
            } else {
                for spacie in self.fleet.iter_mut() {
                    spacie.x = ((spacie.x as i32) + self.direction) as usize;
                }
            }
            return true;
        }
        false
    }
    pub fn all_killed(&self) -> bool {
        self.fleet.is_empty()
    }
    pub fn reached_bottom(&self) -> bool {
        self.fleet
            .iter()
            .map(|spacies| spacies.y)
            .max()
            .unwrap_or(0)
            >= NUM_ROWS - 1 // spacies.y might have to change to spacie.y
    }
    pub fn kill_spacie_at(&mut self, x: usize, y: usize) -> bool {
        if let Some(idx) = self
            .fleet
            .iter()
            .position(|spacie| (spacie.x == x) && (spacie.y == y))
        {
            self.fleet.remove(idx);
            true
        } else {
            false
        }
    }
}

impl Drawable for Spacies {
    fn draw(&self, frame: &mut Frame) {
        // Clear only the parts of the frame where the Spacies will be or have been.
        for spacie in self.fleet.iter() {
            frame[spacie.x][spacie.y] = "  "; // Two spaces to clear a potentially double-width emoji

            // If the Spacies moved downwards, clear the row above as well.
            if spacie.y > 0 {
                frame[spacie.x][spacie.y - 1] = "  ";
            }
        }

        // Move spacies
        for spacie in self.fleet.iter() {
            frame[spacie.x][spacie.y] = if (self.move_timer.time_left.as_secs_f32()
                / self.move_timer.duration.as_secs_f32())
                > 0.5
            {
                "👽"
            } else {
                "👾"
            };
        }
    }
}
