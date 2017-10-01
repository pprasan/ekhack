import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

public class Utils {

    private static PrintWriter out = null;

    private static PrintWriter err = null;

    public static PrintWriter utfStdOut() {
        try {

            if(out == null)
                out = new PrintWriter( new OutputStreamWriter(System.out, "UTF-8"), true);

            return out;

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return null;

    }

    public static PrintWriter utfStdErr() {
        try {

            if(err == null)
                err = new PrintWriter(new OutputStreamWriter(System.err, "UTF-8"), true);

            return err;

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return null;

    }
}
