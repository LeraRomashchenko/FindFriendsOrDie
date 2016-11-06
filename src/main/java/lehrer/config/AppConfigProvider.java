package lehrer.config;

import java.io.File;
import java.util.Properties;

/**
 * Created by Lera on 06.11.2016.
 */
public class AppConfigProvider extends PropertiesProvider<AppConfig> {

    public AppConfigProvider(File authStateFile) {
        super(authStateFile);
    }

    @Override
    protected Properties toProps(AppConfig appConfig) {
        throw new Error("appconfig is read-only");
    }

    @Override
    protected AppConfig fromProps(Properties properties) {
        try {
            return new AppConfig(
                    properties.getProperty("secret"),
                    Integer.parseInt(properties.getProperty("appId")),
                    properties.getProperty("userCode")
            );
        } catch (NumberFormatException e) {
            return new AppConfig(null, -1, null);
        }
    }

}
