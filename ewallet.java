import java.util.*;
import java.io.*;
import java.time.*;

public class Ewallet{

    public static void main(String[] args) throws FileNotFoundException, IOException{

        int opt = 0;
        Scanner read = new Scanner(System.in);
        Account currAccount = null;

        //User interface or main is a constant loop
        //Start off with a option screen which user can then select to perform
        //Application terminates only when user selects to exit
        //Next loop starts once a process is done and the options are displayed again
        //Each process is a conditional and only runs when prompted
        do{

            //Launch Screen
            System.out.println("1. Login\n2. Create Account\n3. Exit\nEnter option number to continue: ");
            opt = read.nextInt();

            //Login
            //Prompt a new option screen
            //Process finish only when logged out
            if(opt == 1){
                String phone = "";
                System.out.println("Phone Number: ");
                phone = read.next();
                boolean found = false;

                //Phone number is used as username here, similar to Whatsapp
                File file = new File("accountdb.txt");
                Scanner sc = new Scanner(file);
                //Search for matching phone number in the database and fetch its account details if found
                //Initialize an account object to hold the user data
                while(sc.hasNextLine()){
                    String line = sc.nextLine();
                    List<String> list = new ArrayList<String>(Arrays.asList(line.split(";")));
                    if(phone.equals(list.get(4))){
                        currAccount = new Account(list);
                        found = true;
                    }
                }
                //Prints error message when account not found
                if(found == false){
                    System.out.println("Invalid phone number. Account not found.\n");
                }
                //Call homescreen method and pass the object created to it
                else{
                    menu(currAccount);
                }
            }

            //Create Account
            else if(opt == 2){
                //Initialize an account object with empty string values
                List<String> init = new ArrayList<String>(){{
                    add("");
                    add("");
                    add("");
                    add("");
                    add("");
                    add("");
                    add("");
                }};
                currAccount = new Account(init);
                String input = "";

                //Take input from user and create a new record in database
                FileWriter fw = new FileWriter("accountdb.txt", true);
                for(String detail: currAccount.detail.subList(0, 5)){
                    System.out.println(detail + ": ");
                    input = read.next();
                    fw.write(input);
                    fw.write(";");
                }
                //Date created and balance initialized by system
                fw.write(LocalDate.now().toString());
                fw.write(";0.00\n");
                fw.flush();
                System.out.println("Account created successfully\n\n\n");
            }

            else if(opt == 3){
                System.exit(0);
            }

        }while(opt != 3);
    }

    //Method to create home screen frame that runs on main
    //Home screen done as a separate method to make the code more readable
    //Account object taken as parameter for main to pass on the initialized account 
    public static void menu(Account currAccount) throws FileNotFoundException, IOException{

        int opt = 0;
        double amount = 0.00;
        Scanner read = new Scanner(System.in);
        
        //Home screen is also a constant loop like main with specific operations to choose from and perform
        do{

            //Home Screen
            //Balance is also displayed here
            System.out.println("\n\n\nBalance: " + String.format("%.2f", Double.parseDouble(currAccount.getBalance())));
            System.out.println("1. Pay\n2. Top Up\n3. Profile Info\n4. Log Out\nEnter option number to continue: ");
            opt = read.nextInt();

            //Pay
            if(opt == 1){
                System.out.println("\n\n\nCurrent balance: " + String.format("%.2f", Double.parseDouble(currAccount.getBalance())) + "\nEnter amount to pay: ");
                amount = read.nextDouble();
                if(amount <= Double.parseDouble(currAccount.getBalance())){
                    currAccount.setBalance(Double.parseDouble(currAccount.getBalance()) - amount);
                    currAccount.updateProfile(String.format("%.2f", Double.parseDouble(currAccount.getBalance())), 7);
                    updateDB(currAccount);
                }
                else{
                    System.out.println("Payment failed due to insufficient balance.");
                }
            }

            //Top Up
            else if(opt == 2){
                System.out.println("\n\n\nCurrent balance: " + String.format("%.2f", Double.parseDouble(currAccount.getBalance())) + "\nEnter amount to top up");
                amount = read.nextDouble();
                currAccount.setBalance(Double.parseDouble(currAccount.getBalance()) + amount);
                currAccount.updateProfile(String.format("%.2f", Double.parseDouble(currAccount.getBalance())), 7);
                updateDB(currAccount);
            }

            //View and edit account info
            else if(opt == 3){
                int no = 0, detailNo;
                String newDetail = "";
                
                //Print account info
                System.out.println("\n\n\n");
                for(String detail : currAccount.getProfile()){
                    System.out.println((no + 1) + ". " + currAccount.detail.get(no) + ": " + detail);
                    no++;
                }
                no = 0;
                
                //Loop constantly to standby and receive inputs from user to edit the account profile
                //Exit only when user selects return
                do{
                    //Users select a specific detail they wish to edit
                    System.out.println("Enter number to edit a specific detail or 0 to return: ");
                    detailNo = read.nextInt();
                    
                    //Exit the profile loop and return to the home screen
                    if(detailNo == 0){
                        break;
                    }
                    
                    //Phone cannot be changed since it functions as a username
                    //User does not have permission to change date created and balance
                    else if(detailNo > 4){
                        System.out.println("This detail cannot be changed");
                    }
                    
                    else{
                        //Prompt for input and update account object along with the database
                        System.out.println("New " + currAccount.detail.get(detailNo - 1) + ": ");
                        newDetail = read.next();
                        currAccount.updateProfile(newDetail, detailNo);
                        updateDB(currAccount);
                        
                        //Print updated account info
                        System.out.println("\n\n\nUpdated Profile: ");
                        for(String detail : currAccount.getProfile()){
                            System.out.println((no + 1) + ". " + currAccount.detail.get(no) + ": " + detail);
                            no++;
                        }
                        no = 0;
                        
                        //Update the specific data field of account object
                        switch(detailNo){
                            case 1:
                                currAccount.setID(newDetail);
                                break;
                            case 2:
                                currAccount.setName(newDetail);
                                break;
                            case 3:
                                currAccount.setIC(newDetail);
                                break;
                            case 4:
                                currAccount.setAddress(newDetail);
                                break;
                        }
                    }
                }while(detailNo != 0);
            }

            //Clear the data in the account object
            else if(opt == 4){
                currAccount = null;
                System.out.println("\n\n\n");
            }

        }while(opt != 4);   
    }

    //Method to overwrite database done separately as it is slightly more complicated
    public static void updateDB(Account currAccount) throws FileNotFoundException, IOException{
        
        File file = new File("accountdb.txt");
        Scanner sc = new Scanner(file);
        FileWriter fw = new FileWriter("temp.txt");
        
        //Copy from database into a temporary file
        //The changed record is handled separately by fetching the values from the account object and overwriting the existing record
        while(sc.hasNextLine()){
            String line = sc.nextLine();
            List<String> list = new ArrayList<String>(Arrays.asList(line.split(";")));
            if(currAccount.getPhone().equals(list.get(4))){
                for(String detail: currAccount.getProfile()){
                    fw.write(detail + ";");
                }
                fw.write("\n");
                fw.flush();
            }
            else{
                fw.write(line + "\n");
                fw.flush();
            }
        }

        //Update the database from the temporary file
        file = new File("temp.txt");
        sc = new Scanner(file);
        fw = new FileWriter("accountdb.txt");
        while(sc.hasNextLine()){
            String line = sc.nextLine();
            fw.write(line + "\n");
        }
        fw.flush();
    }

}

class Account{

    //Data fields
    private String id, name, ic, address, phone, dateCreated, balance;
    //List holding the same data fields so for loop can be used
    private List<String> profile = Collections.<String>emptyList();

    //Name of data fields(const)
    //This list maps to the data fields list and both work together like a table
    public List<String> detail = new ArrayList<String>(){{
        add("ID");
        add("Name");
        add("IC");
        add("Address");
        add("Phone");
        add("Account Creation Date");
        add("Balance");
    }};

    //Constructor that takes in a list as argument
    /*User data is stored in comma-separated-values format. Each line is a record of one user.
      A line is read and converted into a list by splitting the commas*/
    public Account(List<String> profile){
        this.id = profile.get(0);
        this.name = profile.get(1);
        this.ic = profile.get(2);
        this.address = profile.get(3);
        this.phone = profile.get(4);
        this.dateCreated = profile.get(5);
        this.balance = profile.get(6);
        this.profile = profile;
    }

    public void setID(String id){
        this.id = id;
    }

    public void setName(String name){
        this.name = name;
    }

    public void setIC(String ic){
        this.ic = ic;
    }

    public void setAddress(String address){
        this.address = address;
    }

    public void setPhone(String phone){
        this.phone = phone;
    }

    public void setBalance(double balance){
        this.balance = String.valueOf(balance);
    }

    public String getID(){
        return this.id;
    }

    public String getName(){
        return this.name;
    }

    public String getIC(){
        return this.ic;
    }

    public String getAddress(){
        return this.address;
    }
    
    public String getPhone(){
        return this.phone;
    }

    public String getDateCreated(){
        return this.dateCreated;
    }

    public String getBalance(){
        return this.balance;
    }

    public List<String> getProfile(){
        return this.profile;
    }

    public void updateProfile(String newDetail, int detailNo){
        this.profile.set(detailNo - 1, newDetail);
    }

}