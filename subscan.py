import os

# Define banner
banner = """\033[1;31m

  
 __       _       __                 
/ _\_   _| |__   / _\ ___ __ _ _ __  
\ \| | | | '_ \  \ \ / __/ _` | '_ \ 
_\ \ |_| | |_) | _\ \ (_| (_| | | | |
\__/\__,_|_.__/  \__/\___\__,_|_| |_|
                                     

            \033[32m                                  
                           By Bhat Muneeb @bhatmuneeb_
                                                     

\033[32m\033[0m"""

# Print banner
print(banner)

# Prompt the user to enter the target domain
print("\033[32mEnter the target domain:\033[0m", end=" ")
target_domain = input()


# Create a folder with the target domain name
folder_name = f"{target_domain}_output"
os.mkdir(folder_name)

# Change the working directory to the new folder
os.chdir(folder_name)

# Enumerate subdomains using Sublist3r
print("\033[32mEnumerating subdomains using Sublist3r.....\033[0m")
os.system(f"sublist3r -d {target_domain} -o sublist3r.txt")

# Enumerate subdomains using Assetfinder
print("\033[32mEnumerating subdomains using Assetfinder.....\033[0m")
os.system(f"assetfinder --subs-only {target_domain} > assetfinder.txt")

# Enumerate subdomains using findomain
print("\033[32mEnumerating subdomains using findomain.....\033[0m")
os.system(f"findomain -t {target_domain} -u findomain.txt")

# Enumerate subdomains using Subfinder
print("\033[32mEnumerating subdomains using Subfinder......\033[0m")
os.system(f"subfinder -d {target_domain} -o subfinder.txt")

# Enumerate subdomains using Amass passive mode
print("\033[32mEnumerating subdomains using Amass in passive mode...\033[0m")
os.system(f"amass enum -passive -d {target_domain} -o amass_passive.txt")

# Enumerate subdomains using Amass bruteforce mode
print("\033[32mEnumerating subdomains using Amass in bruteforce mode...\033[0m")
os.system(f"amass enum -brute -d {target_domain} -o amass_bruteforce.txt")

# Combine all subdomain lists and remove duplicates
print("\033[32mCombining subdomain lists and removing duplicates...\033[0m")
os.system("cat *.txt | sort -u > subdomains.txt")

# Check for alive subdomains using httprobe
print("\033[32mChecking for alive subdomains using httprobe...\033[0m")
os.system(f"cat subdomains.txt | httprobe > alive_subdomains_httprobe.txt")

# Check for alive subdomains using httpx
print("\033[32mChecking for alive subdomains using httpx...\033[0m")
os.system(f"httpx -l subdomains.txt -o alive_subdomains_httpx.txt")

# Combine the results from both tools
os.system("cat alive_subdomains_httprobe.txt alive_subdomains_httpx.txt | sort -u > alive_subdomains.txt")



#Check for subdomain takeover using Subjack
if os.path.exists("alive_subdomains.txt"):
    print("\033[32mChecking for subdomain takeover using Subjack...\033[0m")
    os.system(f"subjack -w alive_subdomains.txt -t 100 -timeout 30 -v -o subjack_results.txt")


# Check for subdomain takeover using Subzy
if os.path.exists("alive_subdomains.txt"):
    print("\033[32mChecking for subdomain takeover using Subzy...\033[0m")
    os.system(f"subzy r --targets alive_subdomains.txt")

