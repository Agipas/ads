public class DiscntInputData {

    private int[] prices;

    private int discountPercentage;

    public int[] getPrices() {
        return prices;
    }

    public void setPrices(int[] prices) {
        this.prices = prices;
    }

    public int getDiscountPercentage() {
        return discountPercentage;
    }

    public void setDiscountPercentage(int discountPercentage) {
        this.discountPercentage = discountPercentage;
    }

    public DiscntInputData(int[] prices, int discountPercentage) {
        this.prices = prices;
        this.discountPercentage = discountPercentage;
    }
}
