'''
>[!Note] This tool is supposed to do the repetitive task i keep doing when conducting penetration testing. </br>
>[Note] Decompile code with newer jetpack compose package/framework with `--no-res` option in order to execlude resource from update via this command `apktool d quills.apk -o quills --no-res`
# Ideas Logs
1. Create a script to automate the process of building an apk, zipaligning it and signing it
  1. Start by very basic steps
  2. Make sure required tools are already installed (`zipalign`, `apksigner`, etc)
  3. Consider possible errors that may appear
    1. Make sure you create a keystore (assuming no one is there) and include default username & password;
        - Insure you include its steps correctly
        - Add it to the root directory `/` 
        - Only run it once, or just prompt the user for the option if he wants
        - Check if there's a keystore already generated (look it up)
  4. Test it repeatdly
  5. Add also the step of reinstalling the apk to the device/emulator 
     - Make sure you do it correctly and include all required steps
  6. Create output directory with the apk name to include all output files from the previous steps (e.g., if app name is loader, then create and ouput directory for loader that includes loaderZipalign.apk, loaderSigned.apk if you will for better organization) 
'''

'''
Bash vs Python

Bash is good when dealing with commands that I am going to run manually, no extra abstraction
, no dependency management overhead. It's good for a linear pipeline.

Bash is bad when script grows in complexity overtime. If:
  1. Add conditional logic overtime 
  2. Handle errors
  3. Parse structured output (XML)
  4. Build interactive menu

Meanwhile, Python can give the best of the two worlds. 
We can call same terminal commands via subprocess, get proper error handling, cleaner logic flow
, easier string/file manipulation, and the ability to grow with the tool. 

'''