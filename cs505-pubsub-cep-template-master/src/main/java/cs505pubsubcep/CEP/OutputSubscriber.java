package cs505pubsubcep.CEP;

import io.siddhi.core.util.transport.InMemoryBroker;
import net.minidev.json.JSONObject;

import com.google.gson.JsonParser;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;

import java.util.ArrayList;

import java.io.File;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.nio.IntBuffer;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.util.Scanner;

import java.util.HashMap;
import java.util.Map;


public class OutputSubscriber implements InMemoryBroker.Subscriber {

    private String topic;

    public OutputSubscriber(String topic, String streamName) {
        this.topic = topic;
    }

    HashMap<String, Long> zipcode_counts_prev = new HashMap<String, Long>();
    HashMap<String, Long> pos_neg_counts = new HashMap<String, Long>();
    int count_offset = 27; //string index offset to get to the first character that is the count at a particular zipcode
    @Override
    public void onMessage(Object msg) {
        try {
            // output message
            System.out.println();
            System.out.println("OUTPUT CEP EVENT: " + msg);
            System.out.println();

            //Step 1. get message as json_array/object
            
            JsonArray curr_json_msg = new JsonParser().parse(String.valueOf(msg)).getAsJsonArray();
            // return variables
            ArrayList<String> ziplist = new ArrayList<String>();
            
            File f = new File("testcount.txt");
            Scanner scanner = new Scanner(f);
            Long positive = scanner.nextLong();
            Long negative = scanner.nextLong();
            scanner.close();
            
            System.out.println("first positive: " + positive + " negative: " + negative);

            //Step 2 get counts of all zipcodes
            HashMap<String, Long> zipcode_counts_curr = new HashMap<String, Long>();
            for(JsonElement line : curr_json_msg){
                // RTR 2
                String zipcode = line.getAsJsonObject().get("event").getAsJsonObject().get("zip_code").toString();
                if(zipcode_counts_curr.containsKey(zipcode)){
                    zipcode_counts_curr.put(zipcode, zipcode_counts_curr.get(zipcode)+Long.valueOf(1));
                }
                else {
                    zipcode_counts_curr.put(zipcode, Long.valueOf(1));
                }

                // RTR 3
                String test_count_value = line.getAsJsonObject().get("event").getAsJsonObject().get("testcount").toString();
                System.out.println(test_count_value);
                if(test_count_value.equals("\"1\"")){
                    // increment positive
                    positive++;
                }
                else {
                    // incremement nagative
                    negative++;
                }
            }
            
            //Step 3. check msg if any zipcode counts from last batch have doubled 
            for(Map.Entry<String, Long> entry_previous : zipcode_counts_prev.entrySet()){
                String key_prev = entry_previous.getKey();
                Long value_prev = entry_previous.getValue();
                
                if(zipcode_counts_curr.containsKey(key_prev) /*&& zipcode_counts_curr.get(key_prev)*2 >= value_prev*/){               
                    // store zip variable ziplist
                    ziplist.add(key_prev);         
                }
            }

            //3. store ziplist data 
            System.out.println("ziplist"+ziplist);
            // write zipalertlist
            FileWriter writer = new FileWriter("zipalertlist.txt"); 
            for(String str: ziplist){
                writer.write(str.substring(1, str.length()-1) + System.lineSeparator());
            }
            writer.close();

            // write testcount 
            FileWriter writer_testcount = new FileWriter("testcount.txt"); 
            writer_testcount.write(positive + System.lineSeparator());
            writer_testcount.write(negative + System.lineSeparator());
            writer_testcount.close();

            //4. update current zipcode and counts
            zipcode_counts_prev = zipcode_counts_curr;

            System.out.println("positive: " + positive + " negative: " + negative);

        } catch(Exception ex) {
            ex.printStackTrace();
           
        }

    }

    @Override
    public String getTopic() {
        return topic;
    }

}
