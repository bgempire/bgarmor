use std::path::Path;
use clap::{Arg, App};
use std::fs;
use json;

fn main() {
    let config_file = "./launcher.json";
    let config = Path::new(config_file);
    
    let matches = App::new("BGArmor Launcher")
        .version("0.1.0")
        .author("Joel Gomes da Silva <joelgomes1994@hotmail.com>")
        .about("BGE and UPBGE source code obfuscator and launcher toolchain.")
        .arg(Arg::with_name("console")
            .short("c")
            .long("console")
            .help("Enable console window"))
        .arg(Arg::with_name("log")
            .short("l")
            .long("log")
            .help("Log messages in console"))
        .arg(Arg::with_name("args")
            .short("a")
            .long("args")
            .takes_value(true)
            .help("Pass arguments to engine executable (in quotes)"))
        .get_matches();
    
    if config.exists() {
        
        let config = json::parse(
            fs::read_to_string(config)
            .expect("X Could not read launcher.json")
            .as_str())
            .unwrap();
            
        if matches.is_present("args") {
            println!("{}", matches.value_of("args").unwrap());
        }
        println!("{}: {}", config["GameName"], matches.is_present("args"));
        
    } else {
        println!("X Could not find file launcher.json");
    }
}
