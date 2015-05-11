package input;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.Arrays;

public class KeyInput implements KeyListener
{
	private static int MAX_QUEUE=1000;
	private boolean[] keysDown = new boolean[256];
	
	private ArrayList<KeyEvent> events = new ArrayList<KeyEvent>();
	
	public boolean isKeyDown(int keyCode)
	{
		if(keyCode>=keysDown.length)
		{
			return false;
		}
		return keysDown[keyCode];
	}

	public void keyTyped(KeyEvent e)
	{
		// Do nothing
	}

	public void keyPressed(KeyEvent e)
	{
		updateKey(e,true);
	}

	public void keyReleased(KeyEvent e)
	{
		updateKey(e,false);
	}
	
	public boolean hasNext()
	{
		return !events.isEmpty();
	}
	
	public KeyEvent getKeyEvent()
	{
		if(events.isEmpty())
		{
			return null;
		}
		else
		{
			return events.remove(0); // This behavior is like a queue, but it doesn't develop memory leaks.
		}
	}
	
	private void updateKey(KeyEvent e, boolean pressed)
	{	
		events.add(e);
		if(events.size() > MAX_QUEUE)
		{
			events.remove(0);
		}
		if(e.getKeyCode()>=keysDown.length)
		{
			keysDown=Arrays.copyOf(keysDown, e.getKeyCode()+1);
		}
		keysDown[e.getKeyCode()] = pressed;
	}
	
}
