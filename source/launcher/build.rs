extern crate winres;

fn main() {
  if cfg!(target_os = "windows") {
    let mut res = winres::WindowsResource::new();
    res.set_icon("../icons/icon-launcher.ico");
    res.set_manifest_file("./bgarmor.manifest.xml");
    res.compile().unwrap();
  }
}
