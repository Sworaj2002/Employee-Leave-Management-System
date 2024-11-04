Employee Leave Management System Installation and Running Guide

To run the Employee Leave Management System, please follow the steps below:

1. Install the Zip File of Leave Management System.

       Download the zip file containing the leave management system project.
       Extract the contents of the zip file to a desired location on your computer.

2. Download requirements.txt

3. Open your terminal (Command Prompt or PowerShell for Windows, Terminal for macOS/Linux).

        Navigate to the project directory where the requirements.txt file is located.
        Run the command:
        pip install -r requirements.txt
        If you encounter any errors, install the required packages separately.

4. Set Up the Database

        Open MySQL Workbench and run the commands present in database_init.sql to set up the necessary database structure.

5. Open Terminal

        Ensure you are in the project directory where app.py is located.

6. Run the Application

        Start the application by running:
        python app.py

7. Open Any Browser

        It is recommended to use Google Chrome for the best experience.

8. Access the Application

        Open your browser and go to:
        arduino
        http://127.0.0.1:5000/

9. Enjoy the Project

        You can now use the Employee Leave Management System.

10. Login

        For Employee Login:
            Username: employee
            Password: employee123

        For Manager Login:
            Username: manager
            Password: manager123