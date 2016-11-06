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

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.URL;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

public class Main {

    public static void main(String[] args) throws ClientException, ApiException, IOException {
        Logger log = Logger.getLogger("Lehrer"); //тут хотели понять как логировать в файл, а не в консоль
        TransportClient transportClient = new HttpTransportClient();
        VkApiClient vk = new VkApiClient(transportClient);
        AppConfig appConfig = new AppConfigProvider(new File("config.properties")).get();
        //в этом файлике данные для того, чтобы получить токен, их меняют вручную, файлик не заливаем в публичный репозиторий
        try {
            AuthStateProvider authStateProvider = new AuthStateProvider(new File("authConfig.properties"));
            //тут лежит токен и userId, его тоже нельзя заливать в публичный
            AuthState authState = authStateProvider.get();
            if (authState.token == null) { //если нет токена (и userId), то получаем и сохраняем
                AuthResponse authResponse = vk.oauth()
                        .userAuthorizationCodeFlow(appConfig.appId, appConfig.secret, "https://oauth.vk.com/blank.html", appConfig.userCode)
                        .execute();
                authState.token = authResponse.getAccessToken();
                authState.userId = authResponse.getUserId();
                authStateProvider.save(authState);
            }

            UserActor actor = new UserActor(authState.userId, authState.token); //создаем объект для авторизации

            List<UserXtrCounters> users = vk.users().get()
                    .userIds("sayago") //это Тема10
                    .lang(Lang.EN)
                    .execute();

            GetAllResponse photos = vk.photos().getAll(actor) //игрались с получением фоток
                    .ownerId(users.get(0).getId())
                    .lang(Lang.EN)
                    .execute();
            log.info(String.format("found %d photos", photos.getCount()));

            //научилась загружать по урлу с сохранением имени
           ImageDownloader imageDownloader = new ImageDownloader();
           imageDownloader.downloadByUrl("https://pp.vk.me/c620429/v620429807/16f7f/FkqCoTbmZCI.jpg");
        } catch (Exception e) {
            System.err.println(Arrays.toString(e.getStackTrace()));
        }
    }
}
