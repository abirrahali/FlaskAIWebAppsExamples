# BertChatBot

This is Flask web app ChatBot using a BERT model.

![Example Image](Basic-BertChatBot/static/capture.png)

Welcome to the setup guide for our application. This document will walk you through the steps to create a virtual environment, install the necessary requirements, and run the app. Follow these instructions carefully to ensure a smooth setup process.

## Step 1: Create a Virtual Environment


A virtual environment is a self-contained environment where you can install the dependencies for your project without affecting system-wide packages. Follow these steps to create a virtual environment:

1. **Open a Terminal/Command Prompt:** If you're not already in a terminal, open one on your computer.
2. **Navigate to Your Project Directory:** Use the `cd` command to move to the directory where you have stored your project files.
3. **Create a Virtual Environment:** Run the following command to create a virtual environment. Replace `env_name` with the name you want to give your environment.

   ```
   python -m venv env_name
   ```
4. **Activate the Virtual Environment:** Depending on your operating system, you'll need to activate the virtual environment. Here are the commands for various systems:

   macOS and Linux:

   ```
   source env_name/bin/activate
   ```

   Windows:

   ```
   env_name\Scripts\activate
   ```



## Step 2: Install Requirements

Now that your virtual environment is set up, it's time to install the required packages for the app. Make sure your virtual environment is still active, as indicated by the environment name in your terminal prompt. Then, follow these steps:

1. **Navigate to Your Project Directory:** If you're not already in your project directory, use the `cd` command to navigate there in your terminal.
2. **Install Dependencies:** Run the following command to install the required packages from the `requirements.txt` file:

   ```
   pip install -r requirements.txt
   ```

This command will automatically download and install all the necessary packages for your project.



## Step 3: Run the App

With the virtual environment active and the requirements installed, you're ready to run the app. Follow these steps:

1. **Navigate to Your Project Directory:** If you're not already there, use the `cd` command to navigate to your project directory in your terminal.
2. **Run the App:** Execute the command to start your app. The specific command may vary depending on the type of application you are running. Here's a general example:

   ```
   python app.py
   ```


1. Replace `app.py` with the actual name of the Python script that runs your application.
2. **Access the App:** Once the app is running, open a web browser and go to the appropriate URL or access it using the method specified in your app's documentation.
