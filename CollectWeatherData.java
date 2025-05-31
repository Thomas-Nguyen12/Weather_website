// This app is collecting current weather data from an api
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/* To connect to the api, I will use 'spring'
 * 
 */

@SpringBootApplication
public class CollectWeatherData {
    
    
    public static void main(String[] args) {
        System.out.println("This is the weather collection Program"); 
        System.out.println("This is for current data in ELTHAM, UK");

        // I am putting the collection pipeline into 
        System.out.println("Collecting the data..."); 
        try {
            private String apiKey = "4a1f9e155ac6494e98a15506222712";
            String weather_url = "http://api.weatherapi.com/v1/current.json?key=" + apiKey + "&q=London&aqi=yes");
            
            URL url = new URL(weather_url);

            // collecting the data from the API
            

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();

            //Getting the response code
            int responsecode = conn.getResponseCode();

            if (responsecode != 200) {
                System.out.println("Error! Incorrect response code"); 
                System.out.println("Exiting the System");

                // The System.exit() command wll exit the program
                System.exit(1); 
            } else {
                System.out.println("Connection accepted"); 

            }

            // collecting the data now

        } catch(Exception e) {
            System.out.println("----------------------------");
            System.out.println("Error: :");
            System.out.println("----------------------------");
        } finally {
            System.out.println("Finished..."); 
        }
    }
}