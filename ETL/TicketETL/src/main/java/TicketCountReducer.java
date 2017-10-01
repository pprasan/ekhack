import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.regex.Pattern;

public class TicketCountReducer {
    private static PrintWriter out = Utils.utfStdOut();
    private static final Pattern tabSeparator = Pattern.compile("\t");
    private static final Pattern keySeparator = Pattern.compile(":");
    private static HashMap<String, KeyClass> map = new HashMap<>();

    private static class KeyClass {
        public Long numTickets;
        public Double price;

        public KeyClass(Long numTickets, Double price) {
            this.numTickets = numTickets;
            this.price = price;
        }
    }

    public static void main(String[] args) {
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            String line;
            while((line = br.readLine()) != null) {
                try {
                    String[] lineEntries = tabSeparator.split(line);
                    String key = lineEntries[0];
                    String val = lineEntries[1];
                    String[] vals = keySeparator.split(val);
                    Long numTickets = Long.parseLong(vals[0]);
                    Double price = Double.parseDouble(vals[1]);
                    //map.put(key, map.getOrDefault(key, 0L) + val);
                    if(map.containsKey(key)) {
                        KeyClass keyClass = map.get(key);
                        keyClass.numTickets += numTickets;
                        keyClass.price += price;
                    }
                    else {
                        map.put(key, new KeyClass(numTickets, price));
                    }
                }
                catch (Exception e) {}
            }
            map.forEach((key, val) -> {
                String[] keys = keySeparator.split(key);
                out.println(keys[0] + "," + keys[1] + "," + keys[2] + "," + keys[3] + "," +
                        val.numTickets + "," + (val.price / val.numTickets));
            });
        }
        catch (Exception e) {
            //e.printStackTrace();
        }
    }
}
