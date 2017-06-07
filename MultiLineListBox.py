"""
Tkinter Listbox with soft-returns prototype module!
Augusta Nicholas Collins
01703131656
Annotated.
The Listbox pane interface code in MutliLine_Single.__init__ and 
._transmit and .run_selector methods are based on the very useful recipe at 
http://code.activestate.com/recipes/410646-tkinter-listbox-example/
I have revised parts of them and added the multiline string processing,
selection, and extended return functionality.
If you're going to use this, put in a good word for me, yes?
Thank you. <3
"""

import tkinter as Tk


class MutliLine_Single:
    '''A basic Tkinter Listbox single-selection window that allows the use of carriage returns
in its strings. Some extended functionality that replaces falsey list elements with the
`divider_string` argument text. Falsey elements are not selectable.'''

    def __init__(self, frame, items, width=20, divider_string='', return_index=False):
        '''A Listbox selector that allows the use of string entries spanning multiple lines.
Strings are broken on normal line breaks (`\n`). If the pane window is closed or cancelled,
`abort_value` or `None` is returned. Otherwise, the complete, selected value is returned, if
any is selected, else `None`.
 * Confirming with no item selected returns `None` and is different from aborting selection!
    = arguments
items           tuplist of strings      Items to be included in the Listbox list.
                                         - Falsey elements are interpreted as spacers in the list
                                          and are not selectable.
    = optional arguments
width           nonzero positive int    Listbox width, in characters (not px!) (def: 20)
divider_string  string                  Falsey values (including `''`) in the items list will be
                                          replaced with this string when displayed in the Listbox.
                                          In no case are they selectable and clear the current
                                          selection when selected by the user.
                                         - Default: ''
return_index    boolean                 If True, when the Listbox pane is closed, the index value
                                          for the selected item in the `items` argument sequence
                                          will be returned instead of the string itself.
                                         - Be aware that spacer (falsey) list items' indices are
                                          enumerated but are not returnable!
                                         - Returns `None` if no item is selected, as normal.
                                         - Default: False
abort_value     <any>                   If the selector window is closed or cancelled, this value
                                          will be returned. (def: None)
'''
        from tkinter import TOP, RIGHT, LEFT, BOTTOM, Y
        from tkinter import SEL_LAST, SEL_FIRST, END, FIRST
        self.root = frame

        self.lb = lb = Tk.Listbox(frame, selectmode=Tk.SINGLE,
                                  width=width)  # I am working on a MULTIPLE variant of this!
        lb.pack(side=LEFT, fill=Y)

        self.return_index = return_index  # return the item index, rather than the string proper?

        self.index_sets = []
        # ^ A list of Listbox element items and the other lines they're
        #  linked to. When a specific Listbox element is selected, the
        #  index of that selection is matched to the corresponding element
        #  in this list, which contains the indices of the first and last
        #  elements in the Listbox. This range is then selected.

        self.string_register = {}
        # ^ A dict that keys the first Listbox element's selection index
        #  to the whole string. Used to match an selection to an output
        #  on item selection.

        self.null_indices = []
        # ^ A list of index values for blank lines (`''` strings).
        #  All they do is clear the selection.

        self.NULL_MARKER = divider_string or ''
        # ^ If you include blank strings (`''`), they will be replaced
        #  with these characters in the list. Useful organizationally.

        lb_elements = self._parse_strings(items)
        # ^ Get a list of divided strings to put in the Listbox.
        print(lb_elements)
        lb.insert(0, *lb_elements)

        self.lastselection = None  # the last Listbox item selected.

        lb.bind('<<ListboxSelect>>', self._reselect)

        tp = ('test', 'Hello\nWorld\n!!!')
        self._insert(tp)

    def _parse_strings(self, string_list):
        '''Accepts a list of strings and breaks each string into a series of lines,
logs the sets, and stores them in the item_roster and string_register attributes.'''
        index_sets = self.index_sets
        register = self.string_register
        REG_INDEX = self.return_index  # register the item's index in the string list if truey.

        all_lines = []  # holds all strings after lines are split. used for Lb elements.
        line_number = self.lb.index(Tk.END)
        for n, item in enumerate(string_list):  # string_register: `n` is saved if REG_INDEX, else `item`
            if not item:  # null strings or falsey elemetns add a blank space. useful organizationally.
                self.null_indices.append(line_number)  # record the blank position
                all_lines.append(self.NULL_MARKER)  # add the divider text (or '')
                index_sets.append(None)  # add an index value for the gap

                line_number += 1  # increment the line number.
                continue

            lines = item.splitlines()

            all_lines.extend(lines)  # add the divided string to the string stack
            register[line_number] = n if REG_INDEX else item
            # ^ Saves this item keyed to the first Listbox element it's associated with.
            #  Register the string_list index if REG_INDEX, otherwise register the unbroken string.
            #  Dividers are not registered.

            qty = len(lines)
            if qty == 1:  # single line item..
                index_sets.append((line_number, line_number))
            else:  # multiple lines in this item..
                element_range = line_number, line_number + qty - 1  # the range of Listbox indices..
                index_sets.extend([element_range] * qty)  # ..one for each line in the Listbox.

            line_number += qty  # increment the line number.

        return all_lines

    def _reselect(self, event=None):
        "Called whenever the Listbox's selection changes."
        selection = self.lb.curselection()  # Get the new selection data.
        if not selection:  # if there is nothing selected, do nothing.
            self.lastselection = None
            return

        if selection[0] in self.null_indices:  # selected a divider..
            self._clear()  # ..so clear the current selection.
            return

        lines_st, lines_ed = self.index_sets[selection[0]]
        # ^ Get the string block associated with the current selection.

        if lines_st == self.lastselection:
            self._clear()
            return  # If the new set is the same as the old one, clear it.

        self.lb.selection_set(lines_st, lines_ed)  # select all relevant lines
        self.lastselection = lines_st  # remember what you selected last.

        data = self.lb.get(lines_st, lines_ed)
        retText = ""
        for i in range(len(data)):
            retText += data[i]
        print(retText)

    def _clear(self, event=None):
        "Clears the current selection."
        selection = self.lb.curselection()  # Get the currently selected item(s).
        if not selection:  # Nothing to clear!
            return
        self.lb.selection_clear(selection[0], selection[-1])  # deselect..
        self.lastselection = None  # ..and remember that you deselected!

    def _clear_all(self):
        self.lb.delete(0, Tk.END)

    def _insert(self, items):
        lb_elements = self._parse_strings(items)
        self.lb.insert(Tk.END, *lb_elements)
        pass

