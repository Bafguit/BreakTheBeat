package com.fastcat.assemble;

import com.badlogic.gdx.backends.lwjgl3.Lwjgl3Application;
import com.badlogic.gdx.backends.lwjgl3.Lwjgl3ApplicationConfiguration;
import com.fastcat.assemble.WaktaAssemble;

// Please note that on macOS your application needs to be started with the -XstartOnFirstThread JVM argument
public class DesktopLauncher {
	public static void main (String[] arg) {
		Lwjgl3ApplicationConfiguration config = new Lwjgl3ApplicationConfiguration();
		config.setForegroundFPS(60);
		config.setResizable(false);
		config.setWindowedMode(1280, 720);
		config.setBackBufferConfig(8, 8, 8, 8, 16, 0, 20);
		config.setTitle("WaktaverseAssemble");
		new Lwjgl3Application(new WaktaAssemble(), config);
	}
}
