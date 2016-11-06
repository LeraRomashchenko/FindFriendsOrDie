package lehrer.config;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Created by Lera on 06.11.2016.
 */
abstract class PropertiesProvider<T> {

    private File authStateFile;

    PropertiesProvider(File authStateFile) {
        this.authStateFile = authStateFile;
    }

    protected abstract Properties toProps(T obj);
    protected abstract T fromProps(Properties properties);

    public T get() throws IOException {
        try(FileInputStream fileInputStream = new FileInputStream(authStateFile)) {
            Properties properties = new Properties();
            properties.load(fileInputStream);
            return fromProps(properties);
        }
    }

    public void save(T obj) throws IOException {
        try(FileOutputStream fileOutputStream = new FileOutputStream(authStateFile)) {
            Properties properties = toProps(obj);
            properties.store(fileOutputStream, null);
        }
    }
}
