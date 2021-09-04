//Youtube: Android to PC Java Sockets Tutorial Android Studio

package com.example.myclient2;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.util.Log;// to log information on the screen
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    EditText e1;
    public static Socket s = null;
    public static PrintWriter printWriter = null;
    private static final String TAG = "Adnan's Message";
    public static String ip = "192.168.1.106";//R-Pi:146, iPhone:133

    public static boolean forward;
    public static boolean back;
    public static boolean left;
    public static boolean right;
    public Thread myThread;

    public static String param;
    public static boolean param_flag;
    public static boolean command_flag;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Log.i(TAG , "onCreate");
        Button f = (Button) findViewById(R.id.forward_button);
        Button b = (Button) findViewById(R.id.back_button);
        Button l = (Button) findViewById(R.id.left_button);
        Button r = (Button) findViewById(R.id.right_button);

        forward = false;
        back = false;
        left = false;
        right = false;
        param_flag = false;
        command_flag = false;

        myThread = new command_thread();
        myThread.start();

        f.setOnTouchListener(
                new Button.OnTouchListener() {
                    @Override
                    public boolean onTouch (View v, MotionEvent event){
                        if (event.getAction() == MotionEvent.ACTION_DOWN) {
                            forward = true;
                            System.out.println("Action down");
                        }
                        else if (event.getAction() == MotionEvent.ACTION_UP) {
                            forward = false;
                        }
                        System.out.println("In Line 63: After Action up and down");
                        return false;
                    }
                }
        );

        b.setOnTouchListener(
                new Button.OnTouchListener() {
                    @Override
                    public boolean onTouch (View v, MotionEvent event){
                        if (event.getAction() == MotionEvent.ACTION_DOWN) {
                            back = true;
                        }
                        else if (event.getAction() == MotionEvent.ACTION_UP) {
                            back = false;
                        }
                        System.out.println("In Line 63: After Action up and down");
                        return false;
                    }
                }
        );

        l.setOnTouchListener(
                new Button.OnTouchListener() {
                    @Override
                    public boolean onTouch (View v, MotionEvent event){
                        if (event.getAction() == MotionEvent.ACTION_DOWN) {
                            left = true;
                        }
                        else if (event.getAction() == MotionEvent.ACTION_UP) {
                            left = false;
                        }
                        System.out.println("In Line 63: After Action up and down");
                        return false;
                    }
                }
        );

        r.setOnTouchListener(
                new Button.OnTouchListener() {
                    @Override
                    public boolean onTouch (View v, MotionEvent event){
                        if (event.getAction() == MotionEvent.ACTION_DOWN) {
                            right = true;
                        }
                        else if (event.getAction() == MotionEvent.ACTION_UP) {
                            right = false;
                        }
                        return false;
                    }
                }
        );
    }

    public void close_socket(View v){
        printWriter.close();
        try {
            s.close();
        } catch (IOException e) {
            System.out.println("Error in Closing Socket");
            e.printStackTrace();
        }

        command_flag = false;
        System.out.println("Socket closed");
        System.out.println("Socket object ="+s);
    }

    public void set_pendulum_angle(View v){
        System.out.println("Inside set_pendulum_angle()");
        EditText p_text = (EditText)findViewById(R.id.pendulum_angle_text);
        param = "p"+p_text.getText().toString();
        param_flag = true;
    }

    public void set_ip(View v){
        EditText i_text = (EditText)findViewById(R.id.ip_text);
        ip=i_text.getText().toString();
        System.out.println("IP Set to "+ip);
    }

    public void set_velocity(View v){
        System.out.println("Inside set_velocity_angle()");
        EditText v_text = (EditText)findViewById(R.id.velocity_text);
        param = "v"+v_text.getText().toString();
        param_flag = true;
    }
    public void initialise_comm(View v){
        command_flag = true;
    }
     public class command_thread extends Thread implements Runnable{
        @Override
        public void run(){
            while(true) {
                while (!command_flag) { //infinite empty loop
                }
                try {
                    s = new Socket(ip, 6000);
                } catch (IOException e) {
                    //Toast.makeText(getApplicationContext(),"No Server Detected!",Toast.LENGTH_SHORT).show();
                    e.printStackTrace();
                    System.out.println("Error in socket creation");
                }
                try {
                    printWriter = new PrintWriter(s.getOutputStream());
                } catch (IOException e) {
                    System.out.println("Error in printwriter");
                    e.printStackTrace();
                }

                while (command_flag) {
                    if (forward) {
                        if (forward && !left && !right) {
                            System.out.println("w");
                            send_text("w");
                        } else if (forward && left) {
                            System.out.println("q");
                            send_text("q");
                        } else if (forward && right) {
                            System.out.println("e");
                            send_text("e");
                        }
                    } else if (back) {
                        if (back && !left && !right) {
                            System.out.println("s");
                            send_text("s");
                        } else if (back && left) {
                            System.out.println("z");
                            send_text("z");
                        } else if (back && right) {
                            System.out.println("x");
                            send_text("x");
                        }
                    } else if(right){
                        send_text("d");
                    } else if(left){
                        send_text("a");
                    }
                    else {
                        send_text("h");
                    }
                    try {
                        Thread.sleep(200);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    if (param_flag) {
                        send_text(param);
                        param_flag = false;
                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }
         public void send_text(String c){
           /*  try {
                 if (s == null)
                     s = new Socket(ip, 6000);
             } catch (IOException e) {
                 System.out.println("Socket Connection already exists");
             }

             try {
                 printWriter = new PrintWriter(s.getOutputStream());
             } catch (IOException e) {
                 System.out.println("Error in output stream");
             }*/
             printWriter.write(c);
             printWriter.flush();
         }
    }
}