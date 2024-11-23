# User Threat Intelligence Tool Automation

<br>

## Description

Using python as the base language to automate two osint tools to gather information on any user while comparing results to visualize similarities in findings.
**Additional Changes:** using DetectDee via username, email and phoneno and comparing their results with ne another.

<br>

> [!NOTE]
> This project was created for educational purposes. OSINT tasks were executed on dummy accounts.

<br>

## User Threat Intelligence Tools

The following tools used in the project are listed below:

- Sherlock
- DetectDee

<br>

## Python Libraries and Frameworks

The following were used to create the GUI and visualize the results

- **matplotlib**: for creating static, interactive, and animated visualizations
- **Tkinter**: to construct basic graphical user interface (GUI) applications

### ⚙️ Matplotlib Setup

```
pip install matplotlib
```

### ⚙️ Tkinter Setup

```
sudo apt-get install python3-tk
```

## Sherlock

Sherlock, a powerful command line tool used to find usernames across many social networks.

> [!NOTE]
> Before installing Sherlock, we must install python by the following commands:
>
> ```
> sudo apt install python3
> ```

### ⚙️ Setup

Write the following code to install the tool on Kali:

Clone the repository:

```
git clone https://github.com/sherlock-project/sherlock.git
```

Navigate to the directory:

```
cd sherlock
```

Install the requirements:

```
python3 -m pip install -r requirements.txt
```

Use `python3 sherlock --help` to list all possible commands that can be used.

For further help, you may refer to the [Sherlock](https://github.com/sherlock-project/sherlock) repository.

<br>

## DetectDee

DetectDee is a tool that allows hunting down social media accounts by username, email or phone across social networks.

> [!NOTE]
> Before installing DetectDee, we must install golang by the following commands:
>
> ```
> sudo apt update && sudo apt install golang
> ```

### ⚙️ Setup

Write the following code to install the tool on Kali:

```
git clone https://github.com/piaolin/DetectDee.git
cd DetectDee
go mod tidy
go run .
```

For further help, you may refer to [DetectDee](https://github.com/piaolin/DetectDee)).

<br>

After all the above installation just make sure all the intalled files are in the same directory and you can then just enter the command:

```
python3 osint_gui_2.py
```
