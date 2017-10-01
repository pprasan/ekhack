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
    private static HashMap<String, Long> map = new HashMap<>();
    public static void main(String[] args) {
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            String line;
            while((line = br.readLine()) != null) {
                try {
                    String[] lineEntries = tabSeparator.split(line);
                    String key = lineEntries[0];
                    Long val = Long.parseLong(lineEntries[1]);
                    map.put(key, map.getOrDefault(key, 0L) + val);
                }
                catch (Exception e) {}
            }
            map.forEach((key, val) -> {
                String[] keys = keySeparator.split(key);
                out.println(keys[0] + "," + keys[1] + "," + keys[2] + "," + keys[3] + "," + val);
            });
        }
        catch (Exception e) {
            //e.printStackTrace();
        }
    }
}
