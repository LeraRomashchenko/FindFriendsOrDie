package lehrer;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;

/**
 * Created by Lera on 07.11.2016.
 */
public class ImageDownloader {
    //TODO Lera распарсить photos до урлов, научиться выбирать размер скачиваемого (или скачивать только максимального размера)

    public void downloadByUrl(String urlString) {
        try {
            URL url = new URL(urlString);
            BufferedImage image = ImageIO.read(url);
            String imageName = getName(urlString);
            String imageFormat = getExtensionFromName(imageName);
            File outputfile = new File(imageName);
            ImageIO.write(image, imageFormat, outputfile);
        } catch (IOException e) {
        }
    }

    private String getName(String url) {
        String[] splitedUrl = url.split("/");
        return splitedUrl[splitedUrl.length-1];
    }

    private String getExtensionFromName(String name)
    {
        return name.split("\\.")[1];
    }
}
