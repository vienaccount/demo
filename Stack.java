package demo.test;

/**
 * Stack.
 * 
 * @author Vincent Tran
 * @created Oct 17, 2023
 *
 */

import java.util.Arrays;

public class Stack
{
	private Object[] elements;

	private int top = 0;

	public Stack()
	{
		super();
		elements = new Object[10];
	}

	public Stack(int initialSize)
	{
		super();
		elements = new Object[initialSize];
	}

	public boolean isEmpty()
	{
		return top == 0;
	}

	public void push(Object element)
	{
		if (top == elements.length)
		{
			elements = Arrays.copyOf(elements, elements.length + 10);
		}
		elements[top] = element;
		top++;
	}

	public Object pop()
	{
		if (!isEmpty())
		{
			return elements[--top];
		}
		return null;
	}
}
