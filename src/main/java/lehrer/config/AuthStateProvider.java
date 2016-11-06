package lehrer.config;

import java.io.File;
import java.util.Properties;

/**
 * Created by Lera on 06.11.2016.
 */
public class AuthStateProvider extends PropertiesProvider<AuthState> {

    public AuthStateProvider(File authStateFile) {
        super(authStateFile);
    }

    @Override
    protected Properties toProps(AuthState authState) {
        Properties properties = new Properties();
        properties.setProperty("token", authState.token);
        properties.setProperty("userId", Integer.toString(authState.userId));
        return properties;
    }

    @Override
    protected AuthState fromProps(Properties properties) {
        try {
            return new AuthState(
                    properties.getProperty("token"),
                    Integer.parseInt(properties.getProperty("userId"))
            );
        } catch (NumberFormatException e) {
            return new AuthState(null, -1);
        }
    }

}
