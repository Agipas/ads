public class Hamster {

    private long hunger;

    private long greed;

    public long getHunger() {
        return hunger;
    }

    public void setHunger(int hunger) {
        this.hunger = hunger;
    }

    public long getGreed() {
        return greed;
    }

    public void setGreed(int greed) {
        this.greed = greed;
    }

    public Hamster(int hunger, int greed) {
        this.hunger = hunger;
        this.greed = greed;
    }

    public long getDailyFoodNeeds(int neighborCount) {
        return hunger + greed * neighborCount;
    }
}
