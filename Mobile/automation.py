'''
>[!Note] This tool is supposed to do the repetitive task i keep doing when conducting penetration testing. </br>
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
'''
