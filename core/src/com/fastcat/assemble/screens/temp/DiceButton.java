package com.fastcat.assemble.screens.temp;

import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.fastcat.assemble.abstrcts.AbstractDice;
import com.fastcat.assemble.abstrcts.AbstractUI;
import com.fastcat.assemble.dices.basic.NormalDice;
import com.fastcat.assemble.dices.legend.Fraud3;
import com.fastcat.assemble.handlers.FileHandler;
import com.fastcat.assemble.handlers.FontHandler;

public class DiceButton extends AbstractUI {

    public AbstractDice dice;

    public DiceButton() {
        this(new NormalDice());
    }

    public DiceButton(AbstractDice dice) {
        super(FileHandler.dice.get("Dice"));
        pix();
        this.dice = dice;
        clickable = false;
    }

    @Override
    protected void renderUi(SpriteBatch sb) {
        if (enabled && dice != null) {
            if (overable && !over) sb.setColor(Color.LIGHT_GRAY);
            if (showImg) sb.draw(dice.img, x, y, width, height);
        }
    }

    @Override
    public void onClick() {
        dice.roll();
    }
}
