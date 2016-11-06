package lehrer.config;

/**
 * Created by Lera on 06.11.2016.
 */
public class AppConfig {
    public String secret;
    public int appId;
    public String userCode;

    public AppConfig(String secret, int appId, String userCode) {
        this.secret = secret;
        this.appId = appId;
        this.userCode = userCode;
    }
}
