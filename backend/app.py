from flask import Flask, request, jsonify, send_from_directory

import paramiko

import time

import os



app = Flask(__name__, static_folder="../frontend")





@app.route("/")

def home():

    return send_from_directory("../frontend", "index.html")





@app.route("/style.css")

def style():

    return send_from_directory("../frontend", "style.css")





@app.route("/script.js")

def script():

    return send_from_directory("../frontend", "script.js")


@app.route("/api/execute", methods=["POST"])
def execute_command():
    data = request.get_json()

    router_ip = data.get("ip", "").strip()
    command = data.get("command", "").strip()

    if not router_ip or not command:
        return jsonify({
            "success": False,
            "message": "Router IP and command are required."
        }), 400

    username = "admin"
    password = "cisco"

    ssh = None

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=router_ip,
            username=username,
            password=password,
            port=22,
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        shell = ssh.invoke_shell()

        time.sleep(1)

        if shell.recv_ready():
            shell.recv(65535)

        shell.send("terminal length 0\n")
        time.sleep(0.5)

        if shell.recv_ready():
            shell.recv(65535)

        shell.send(command + "\n")
        time.sleep(2)

        output = ""

        while shell.recv_ready():
            output += shell.recv(65535).decode(
                "utf-8",
                errors="ignore"
            )
            time.sleep(0.2)

        return jsonify({
            "success": True,
            "output": output
        })

    except paramiko.AuthenticationException:
        return jsonify({
            "success": False,
            "message": "SSH authentication failed."
        }), 401

    except paramiko.SSHException as error:
        return jsonify({
            "success": False,
            "message": "SSH error: " + str(error)
        }), 500

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
