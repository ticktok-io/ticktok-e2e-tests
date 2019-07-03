package io.ticktok.sanity;

import io.ticktok.client.Ticktok;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

import static io.ticktok.client.Ticktok.options;
import static java.lang.Thread.sleep;

public class SanityCheck {

    private static final DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");

    public static void main(String[] args) throws InterruptedException {
        Ticktok ticktok = new Ticktok(options().domain("http://localhost:9643").token("ticktok-zY3wpR"));
        ticktok.schedule("sanity-30", "every.30.seconds", () -> System.out.println(dateFormat.format(new Date()) + " sanity-30"));
        ticktok.schedule("sanity-15", "every.15.seconds", () -> System.out.println(dateFormat.format(new Date()) + " sanity-15"));
        ticktok.schedule("sanity-1", "every.1.minutes", () -> System.out.println(dateFormat.format(new Date()) + " sanity-1"));
        sleep(5000);
        ticktok.tick("sanity-1", "every.1.minutes");
    }
}
