package top.dkvirus.novel.models;

import java.util.ArrayList;
import java.util.List;

public class NovelVo extends CommonVo {

    private Novel data = new Novel();

    public Novel getData() {
        return data;
    }
    public void setData(Novel data) {
        this.data = data;
    }
}
