package ticktok.e2e;

import io.ticktok.Ticktok;
import io.ticktok.TicktokOptions;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class TicktokSanityTest {

    @Test
    public void tickOnRegister(){
        new Ticktok(new TicktokOptions("", "")).
                newClock("sanity_clock").
                on("every.5.seconds").
                invoke(() -> {
                    assertTrue(true); // assert callback
                });
    }
}
