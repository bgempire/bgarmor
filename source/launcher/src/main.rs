use std::path::Path;
use std::env;
use clap::{Arg, App};
use std::fs;
// use subprocess::Popen;


fn main() {
    
    let matches = App::new("BGArmor Launcher")
        .version("0.0.6")
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
        
    
    let cur_os = if env::consts::FAMILY == "windows" {"Windows"} else {"Linux"};
    let executables = get_executables(cur_os);
    if executables.len() == 2 {
        for el in executables {
            println!("{}", el);
        }
        if matches.is_present("a") {
        }
    } else {
        println!("X Could not find any Python and engine executable")
    }
}


fn get_executables(cur_os: &str) -> Vec<String> {
    let launcher_base_path_str = String::from("./launcher/");
    let python_config_name = "python_executable.txt";
    let engine_config_name = "engine_executable.txt";
    
    let launcher_paths = [
        [launcher_base_path_str.clone().as_str(), cur_os, "32/"].join(""),
        [launcher_base_path_str.clone().as_str(), cur_os, "64/"].join(""),
    ];
    
    for path in launcher_paths {
        let path = String::from(path);
        
        let python_config_path_str = [path.clone(), python_config_name.to_string()].join("");
        let engine_config_path_str = [path.clone(), engine_config_name.to_string()].join("");
        
        let python_config_path = Path::new(&python_config_path_str);
        let engine_config_path = Path::new(&engine_config_path_str);
        
        let python_executable_path_str = get_executable_from_config(&python_config_path).clone();
        let engine_executable_path_str = get_executable_from_config(&engine_config_path).clone();
        let python_executable_path = Path::new(python_executable_path_str.as_str());
        let engine_executable_path = Path::new(engine_executable_path_str.as_str());
        let mut executables: Vec<String> = Vec::new();
        
        if python_executable_path.exists() {
            executables.push(python_executable_path_str.clone());
            
            if engine_executable_path.exists() {
                executables.push(engine_executable_path_str.clone());
                return executables;
            } else {
                println!("X Invalid engine executable path on {}", engine_config_path_str);
            }
        } else {
            println!("X Invalid Python executable path on {}", python_config_path_str);
        }
    }
    return Vec::new();
}

fn get_executable_from_config(config_path: &Path) -> String {
    
    if config_path.exists() {
        let file_data_str = String::from(fs::read_to_string(config_path).expect("").as_str());
        let mut elements: Vec<String> = Vec::new();
        
        for el in file_data_str.split("=") {
            let mut el = String::from(el.clone());
            el = String::from(el.trim());
            el = el.replace("'", "").replace("\"", "");
            elements.push(el);
        }
        
        if elements.len() == 2 {
            let executable_path_str = elements[1].clone();
            let executable_path = Path::new(executable_path_str.as_str());
            
            if executable_path.exists() {
                return executable_path_str;
            }
        }
        return String::from("");
    }
    return String::from("");
}
