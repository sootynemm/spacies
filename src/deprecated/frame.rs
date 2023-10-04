use crate::{NUM_COLS, NUM_ROWS};

pub type Frame = Vec<Vec<&'static str>>;

pub fn new_frame() -> Frame {
    let mut columns = Vec::with_capacity(NUM_COLS); // Renamed from `cols` to `columns`
    for _ in 0..NUM_COLS {
        let mut col = Vec::with_capacity(NUM_ROWS);
        for _ in 0..NUM_ROWS {
            col.push(" ");
        }
        columns.push(col); // Renamed from `cols` to `columns`
    }
    columns // Renamed from `cols` to `columns`
}

pub trait Drawable {
    fn draw(&self, frame: &mut Frame);
}
