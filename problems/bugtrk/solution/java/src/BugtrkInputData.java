public class BugtrkInputData {

    private long bugCount;

    private long sheetWidth;

    private long sheetHeight;

    public long getBugCount() {
        return bugCount;
    }

    public void setBugCount(long bugCount) {
        this.bugCount = bugCount;
    }

    public long getSheetWidth() {
        return sheetWidth;
    }

    public void setSheetWidth(long sheetWidth) {
        this.sheetWidth = sheetWidth;
    }

    public long getSheetHeight() {
        return sheetHeight;
    }

    public void setSheetHeight(long sheetHeight) {
        this.sheetHeight = sheetHeight;
    }

    public BugtrkInputData(long bugCount, long sheetWidth, long sheetHeight) {
        this.bugCount = bugCount;
        this.sheetWidth = sheetWidth;
        this.sheetHeight = sheetHeight;
    }
}
