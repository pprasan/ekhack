import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;

import static org.apache.commons.lang3.StringUtils.isBlank;

public class TicketCountMapper {
    private static PrintWriter out = Utils.utfStdOut();
    private static final Pattern csvPattern = Pattern.compile(",");
    private static final Pattern datePattern = Pattern.compile(" ");

    public static void main(String[] args) {
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            String line;
            while((line = br.readLine()) != null) {
                try {
                    String[] columns = csvPattern.split(line);
                    String orig = columns[8];
                    String dest = columns[10];
                    String departureDateTime = columns[14];

                    if (isBlank(orig) || isBlank(dest) || isBlank(departureDateTime))
                        continue;

                    String departureDate = datePattern.split(departureDateTime)[0];
                    out.println(orig + ":" + dest + ":" + departureDate +
                            "\t" + "1");
                }
                catch (Exception e) {}

            }
        }
        catch (Exception e) {
            //e.printStackTrace();
        }
    }
}
