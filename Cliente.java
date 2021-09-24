import java.net.*;
import java.io.*;
  
public class Cliente
{
    // initialize socket and input output streams
    private Socket socket            = null;
    private DataInputStream  input   = null;
    private DataOutputStream out     = null;
  
    // constructor to put ip address and port
    public Cliente(String address, int port)
    {
        // establish a connection
        try
        {
            int n = 0;
            while(n<25){
            socket = new Socket(address, port);
            System.out.println("Conexión " + n);
  
            // takes input from terminal
            input  = new DataInputStream(System.in);
  
            // sends output to the socket
            out    = new DataOutputStream(socket.getOutputStream());
            n++;
            }
        }
        catch(UnknownHostException u)
        {
            System.out.println(u);
        }
        catch(IOException i)
        {
            System.out.println(i);
        }
  
        // string to read message from input
        String line = "";
  
        // keep reading until "Over" is input
        while (!line.equals("Over"))
        {
            try
            {
                line = input.readLine();
                out.writeUTF(line);
            }
            catch(IOException i)
            {
                System.out.println(i);
            }
        }
  
        // close the connection
        try
        {
            input.close();
            out.close();
            socket.close();
        }
        catch(IOException i)
        {
            System.out.println(i);
        }
    }
  
    public static void main(String args[])
    {
        Cliente client = new Cliente("192.168.85.128", 5000);
    }
}