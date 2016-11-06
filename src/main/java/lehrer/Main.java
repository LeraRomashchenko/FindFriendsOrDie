package lehrer;

import com.vk.api.sdk.client.Lang;
import com.vk.api.sdk.client.TransportClient;
import com.vk.api.sdk.client.VkApiClient;
import com.vk.api.sdk.client.actors.UserActor;
import com.vk.api.sdk.exceptions.ApiException;
import com.vk.api.sdk.exceptions.ClientException;
import com.vk.api.sdk.httpclient.HttpTransportClient;
import com.vk.api.sdk.objects.AuthResponse;
import com.vk.api.sdk.objects.photos.responses.GetAllResponse;
import com.vk.api.sdk.objects.users.UserXtrCounters;
import lehrer.config.AppConfig;
import lehrer.config.AppConfigProvider;
import lehrer.config.AuthState;
import lehrer.config.AuthStateProvider;

import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

public class Main {

    public static void main(String[] args) throws ClientException, ApiException, IOException {
        Logger log = Logger.getLogger("Lehrer");
        TransportClient transportClient = new HttpTransportClient();
        VkApiClient vk = new VkApiClient(transportClient);
        AppConfig appConfig = new AppConfigProvider(new File("config.properties")).get();
        try {
            AuthStateProvider authStateProvider = new AuthStateProvider(new File("authConfig.properties"));
            AuthState authState = authStateProvider.get();
            if (authState.token == null) {
                AuthResponse authResponse = vk.oauth()
                        .userAuthorizationCodeFlow(appConfig.appId, appConfig.secret, "https://oauth.vk.com/blank.html", appConfig.userCode)
                        .execute();
                authState.token = authResponse.getAccessToken();
                authState.userId = authResponse.getUserId();
                authStateProvider.save(authState);
            }

            UserActor actor = new UserActor(authState.userId, authState.token);

            List<UserXtrCounters> users = vk.users().get()
                    .userIds("sayago")
                    .lang(Lang.EN)
                    .execute();

            GetAllResponse photos = vk.photos().getAll(actor)
                    .ownerId(users.get(0).getId())
                    .lang(Lang.EN)
                    .execute();
            log.info(String.format("found %d photos", photos.getCount()));
        } catch (Exception e) {
            System.err.println(Arrays.toString(e.getStackTrace()));
        }
    }
}
