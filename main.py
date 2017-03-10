from shapes import *
import random


def main():
    random.seed()

    # Create window
    main_window = Container(0, 600, 0, 200, 25)
    win = GraphWin("Neuron Mitochondria", main_window.xMax, main_window.yMax, autoflush=False)

    # Create label container
    label_width = 100
    labels = Container(main_window.xMax - main_window.buffer - label_width,
                       main_window.xMax - main_window.buffer,
                       main_window.y + main_window.buffer,
                       main_window.yMax - main_window.buffer,
                       10)

    # Mitochondria counter
    text1 = Text(Point(labels.mid.getX(), labels.mid.getY() - labels.buffer), "Mitochondria")
    text2 = Text(Point(labels.mid.getX(), labels.mid.getY() + labels.buffer), "Count: 0")
    mito_count = 0
    text1.draw(win)
    text2.draw(win)

    # Create model
    model_label_buffer = 30
    model = Container(main_window.x + main_window.buffer,
                      main_window.xMax - main_window.buffer - labels.dx() - model_label_buffer,
                      main_window.y + main_window.buffer,
                      main_window.yMax - main_window.buffer,
                      0)

    # Arbitrary height of both halves of neuron body
    neuron_height = model.dy() / 6

    # Draw upper part of neuron
    top_neuron = NeuronPoly(model, model.y + neuron_height, 50, win)
    top_neuron.points.append(Point(model.xMax - model.buffer, model.y))
    top_neuron.points.append(Point(model.x + model.buffer, model.y))
    top_neuron.draw()

    # Draw bottom part of neuron
    bottom_neuron = NeuronPoly(model, model.yMax - model.buffer - neuron_height, 50, win)
    bottom_neuron.points.append(Point(model.xMax - model.buffer, model.yMax))
    bottom_neuron.points.append(Point(model.x + model.buffer, model.yMax))
    bottom_neuron.draw()

    # Set up area for mito to be placed
    # Only allow mito to be within neuron edges
    Mito.container = Container(model.x + model.buffer,
                               model.xMax - model.buffer,
                               top_neuron.avgHeight + top_neuron.maxHeightDev,
                               bottom_neuron.avgHeight - bottom_neuron.maxHeightDev,
                               Mito.mitoHeight)
    Mito.defaultDx = model.dx() / 10000

    # Create mitochondria objects
    mitos = []
    mitos_num = 15
    for i in range(0, mitos_num):
        mitos.append(Mito(win))

    # Run until mouse is clicked
    try:
        while not win.checkMouse():
            for m in mitos:
                # Randomly choose whether to draw new mito
                if not m.drawn:
                    if m.randDraw(10000):
                        mito_count += 1
                        text2.setText("Count: {0}".format(mito_count))
                # Move mito if drawn
                else:
                    m.move()
                    # Reset mito if it's crossed the neuron body
                    if m.checkEnd():
                        mitos.remove(m)
                        mitos.append(Mito(win))
                        mito_count -= 1
                        text2.setText("Count: {0}".format(mito_count))
            # Limit the window refresh so that adding more mito won't slow the simulation down
            update(1000)
        # Pause for click in window
        win.getMouse()
        win.close()
    except GraphicsError as err:
        if "{0}".format(err) != "checkMouse in closed window":
            print("GraphicsError: {0}".format(err))

# Run
if __name__ == "__main__":
    random.seed()
    main()
