use std::io;
#[cfg(windows)]
use winres::WindowsResource;

fn main() -> io::Result<()> {
    #[cfg(windows)]
    {
        WindowsResource::new()
            .set_icon("../icons/icon-launcher.ico")
            .compile()
            .expect("X Could not set icon");
    }
    Ok(())
}
