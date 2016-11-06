package lehrer.config;

/**
 * Created by Lera on 06.11.2016.
 */
public class AuthState {
    public String token;
    public int userId;

    public AuthState(String token, int userId) {
        this.token = token;
        this.userId = userId;
    }
}
