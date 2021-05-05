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

public class OutputSubscriber implements InMemoryBroker.Subscriber {

    private String topic;

    public OutputSubscriber(String topic, String streamName) {
        this.topic = topic;
    }
    
    JsonArray prev_zipCounts = new JsonArray();
    int count_offset = 27;
    @Override
    public void onMessage(Object msg) {
        
        try {
            //Step 1. get message as json_array/object
            JsonArray curr_json_msg = new JsonParser().parse(String.valueOf(msg)).getAsJsonArray();
            ArrayList<String> ziplist = new ArrayList<String>();
            
            //Step 2. check msg if any zipcode counts from last batch have doubled 
            for(int i=0; i < prev_zipCounts.size(); i++){
                JsonElement prev = prev_zipCounts.get(i);
                System.out.println(prev);
        
                String prev_zip_code=prev.getAsJsonObject().get("event").getAsJsonObject().get("zip_code").toString();
                // iterate through prev_zipcounts 
   
                String curr_json_str=curr_json_msg.toString();
                if(/*true*/ curr_json_str.contains("\"zip_code\":\""+prev_zip_code+"\"") ){ 
                    
                    int zipcount_index_start= curr_json_str.indexOf("\"zip_code\":\""+prev_zip_code+"\"");
                    int zipcount_index_end = curr_json_str.indexOf('}', zipcount_index_start);
                    int curr_count= Integer.parseInt(curr_json_str.substring(zipcount_index_start+count_offset,zipcount_index_end));

                    int prev_count = Integer.parseInt(prev.getAsJsonObject().get("event").getAsJsonObject().get("count").toString());
              
                    if (curr_count*2 >= prev_count){
                        // store zip variable ziplist
                        ziplist.add(prev_zip_code);
                    }
                    
                    /*// BLOCK for testing on every incoming patient
                    // 
                    // int zipcount_index_start = curr_json_str.indexOf("\"zip_code\""); //delete me after test
                    // int zipcount_index_end= curr_json_str.indexOf('}', zipcount_index_start);
                    // int curr_count= Integer.parseInt(curr_json_str.substring(zipcount_index_start+count_offset ,zipcount_index_end));
                    // int prev_count = Integer.parseInt(prev.getAsJsonObject().get("event").getAsJsonObject().get("count").toString());
                     
                    // if (true){
                    //     // store zin variable ziplist
                    //     ziplist.add(prev_zip_code);
                    // }
                    //  // --- end of delete
                    */
                    
                }
            }
                           
            //3. store ziplist data 
            System.out.println("ziplist"+ziplist);
            
            FileWriter writer = new FileWriter("zipalertlist.txt"); 
            for(String str: ziplist){
                writer.write(str.substring(1, str.length()-1) + System.lineSeparator());
            }
            writer.close();
            //4. update current zipcode and counts
            prev_zipCounts = curr_json_msg;

            System.out.println();
            System.out.println("OUTPUT CEP EVENT: " + msg);
            System.out.println();

           
            //String[] sstr = String.valueOf(msg).split(":");
            //String[] outval = sstr[2].split("}");
            //Launcher.accessCount = Long.parseLong(outval[0]);

        } catch(Exception ex) {
            ex.printStackTrace();
           
        }

    }

    @Override
    public String getTopic() {
        return topic;
    }

}
