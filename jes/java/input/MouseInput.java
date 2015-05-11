package input;

import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.ArrayList;

public class MouseInput implements MouseListener, MouseMotionListener
{
	private static int MAX_QUEUE=1000;
	
	private int mouseX=0;
	private int mouseY=0;
	private boolean leftMouseDown=false;
	
	private ArrayList<MouseEvent> events = new ArrayList<MouseEvent>();
	
	
	public int getMouseX()
	{
		return mouseX;
	}

	public int getMouseY()
	{
		return mouseY;
	}

	public boolean isLeftMouseDown()
	{
		return leftMouseDown;
	}
	
	public boolean hasNext()
	{
		return !events.isEmpty();
	}
	
	public MouseEvent getMouseEvent()
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
	
	public void mouseDragged(MouseEvent e)
	{
		mouseX=e.getX();
		mouseY=e.getY();
	}

	public void mouseMoved(MouseEvent e)
	{
		mouseX=e.getX();
		mouseY=e.getY();
	}

	public void mouseClicked(MouseEvent e)
	{
		// TODO Auto-generated method stub
		
	}

	public void mousePressed(MouseEvent e)
	{
		updateButton(e,true);
	}

	public void mouseReleased(MouseEvent e)
	{
		updateButton(e,false);
	}
	
	private void updateButton(MouseEvent e, boolean pressed)
	{
		events.add(e);
		if(events.size() > MAX_QUEUE)
		{
			events.remove(0);
		}
		if(e.getButton()==MouseEvent.BUTTON1)
		{
			leftMouseDown=pressed;
		}
	}

	public void mouseEntered(MouseEvent e)
	{
		//Do nothing
		
	}

	public void mouseExited(MouseEvent e)
	{
		//Do nothing
		
	}
	
}
