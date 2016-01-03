public class HamstrInputData {

    private Hamster[] hamsters;

    private long dailyBudget;

    public Hamster[] getHamsters() {
        return hamsters;
    }

    public void setHamsters(Hamster[] hamsters) {
        this.hamsters = hamsters;
    }

    public long getDailyBudget() {
        return dailyBudget;
    }

    public void setDailyBudget(long dailyBudget) {
        this.dailyBudget = dailyBudget;
    }

    public HamstrInputData(long dailyBudget, Hamster[] hamsters) {
        this.hamsters = hamsters;
        this.dailyBudget = dailyBudget;
    }
}
