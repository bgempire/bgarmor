use std::env;
use std::fs;
use std::path::{PathBuf};
use clap::{Arg, App};
use json;
use subprocess::*;

fn main() {
    let matches = App::new("BGArmor Launcher")
        .version("0.1.0")
        .author("Joel Gomes da Silva <joelgomes1994@hotmail.com>")
        .about("BGE and UPBGE source code obfuscator and launcher toolchain.")
        .arg(Arg::with_name("console")
            .short("c")
            .long("console")
            .help("Enable console window"))
        .arg(Arg::with_name("args")
            .short("a")
            .long("args")
            .takes_value(true)
            .help("Pass arguments to engine executable (in quotes)"))
        .arg(Arg::with_name("file")
            .short("f")
            .long("file")
            .takes_value(true)
            .help("Pass project file path to be opened by launcher"))
        .get_matches();
        
    let config = get_config(if matches.is_present("file") {matches.value_of("file").unwrap()} else {""});
    
    if config.has_key("GameName") {
        let executables = get_executables(&config);
        let quote = if env::consts::FAMILY == "windows" {"\""} else {"'"};
        
        if executables.len() == 2 {
            let mut args: Vec<String> = Vec::new();
            
            if matches.is_present("args") {
                args.push("--args".to_string());
                args.push([quote, matches.value_of("args").unwrap(), quote].join("").to_string());
            }
            
            if matches.is_present("file") {
                args.push("--file".to_string());
                args.push([quote, matches.value_of("file").unwrap(), quote].join("").to_string());
            }
            
            run_python_executable(executables, args);
        } else {
            println!("X Could not find any Python and engine executable")
        }
    }
}

/// Get base directory where launcher executable is located.
fn get_base_path() -> std::path::PathBuf {
    let root_path = env::current_exe().unwrap().to_path_buf();
    let root_path = root_path.parent().unwrap().to_path_buf();
    return root_path;
}

/// Read config file from launcher directory and return it as JsonValue.
fn get_config(_file: &str) -> json::JsonValue {
    let mut config_path = if _file.len() > 0 {PathBuf::from(_file)} else {get_base_path()};
    
    if _file.len() == 0 {
        config_path.push("launcher/config.json");
    }
    
    if config_path.exists() && config_path.is_file() {
        let config_data_str = fs::read_to_string(config_path).expect("X Could not read file config.json");
        return json::parse(config_data_str.as_str()).expect("X Could not parse file config.json");
    }
    println!("X Could not find config.json");
    return json::parse("{}").unwrap();
}

/// Get the first existing Python and engine executables from config as a Vec.
fn get_executables(config: &json::JsonValue) -> Vec<String> {
    let launcher_base_path_str: PathBuf = get_base_path();
    let cur_os = if env::consts::FAMILY == "windows" {"Windows"} else {"Linux"};
    let architectures = ["32", "64"];
    
    for architecture in architectures {
        let key_engine = ["Engine", cur_os, architecture].join("");
        let key_python = ["Python", cur_os, architecture].join("");
        
        let path_engine_str = &config[key_engine].as_str().unwrap();
        let path_python_str = &config[key_python].as_str().unwrap();
        let mut path_engine = launcher_base_path_str.clone();
        path_engine.push(path_engine_str);
        let mut path_python = launcher_base_path_str.clone();
        path_python.push(path_python_str);
        
        let mut executables: Vec<String> = Vec::new();
            
        if path_python.is_file() && path_python.exists() {
            path_python.canonicalize().unwrap();
            let path_python_str = path_python.to_str().unwrap();
            executables.push(String::from(path_python_str));
            
            if path_engine.is_file() && path_engine.exists() {
                path_engine.canonicalize().unwrap();
                let path_engine_str = path_engine.to_str().unwrap();
                executables.push(String::from(path_engine_str));
                return executables;
            }
        }
    }
    return Vec::new();
}

// Run the launcher script in the Python executable.
fn run_python_executable(executables: Vec<String>, _args: Vec<String>) {
    
    // Enable executable execution on Linux
    if env::consts::FAMILY != "windows" {
        
        for el in executables.iter() {
            
            let mut _process = Popen::create(&["chmod", "+x", el.as_str()], PopenConfig {
                stdout: Redirection::Pipe, ..Default::default()
            }).expect("X Could not enable execution of Python executable");
            let _exit_status = _process.wait();
        
            let (_out, _err) = _process.communicate(None).unwrap();
            
            if _out != None {
                println!("{}", _out.unwrap());
            }
            
            println!("Enable execution of: {}", el);
        }
    }
    
    let mut launcher_script = get_base_path();
    launcher_script.push("launcher/launcher.py");
    
    if !launcher_script.exists() {
        println!("X Could not find script launcher.py");
        return;
    }
    
    let launcher_script = launcher_script.canonicalize().unwrap();
    
    // Execute launcher script on Python interpreter
    for executable in executables.iter() {
        println!("Run executable: {} {}", executable, launcher_script.to_str().unwrap());
        
        let mut args: Vec<&str> = Vec::from([executable.as_str(), launcher_script.to_str().unwrap()]);
        
        for arg in _args.iter() {
            args.push(arg.as_str());
        }
        
        let mut _process = Popen::create(&args.to_vec() , PopenConfig {
            stdout: Redirection::Pipe, ..Default::default()
        }).expect("X Could not run script launcher.py");
        
        let (out, _err) = _process.communicate(None).unwrap();
        
        if out != None {
            println!("{}", out.unwrap());
        }
        
        let _exit_status = _process.wait().expect("X Could not get exit status");
        println!("Exit success: {}", _exit_status.success());
        return;
    }
}
