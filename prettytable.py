class PrettyTable:
    def __init__(self):
        self.field_names = []
        self._rows = []

    def add_row(self, row):
        self._rows.append(list(row))

    def __str__(self):
        rows = [self.field_names] + self._rows if self.field_names else self._rows
        if not rows:
            return ""
        widths = [max(len(str(row[i])) if i < len(row) else 0 for row in rows) for i in range(max(len(row) for row in rows))]
        def fmt(row):
            return " | ".join(str(row[i]).ljust(widths[i]) if i < len(row) else "".ljust(widths[i]) for i in range(len(widths)))
        lines = []
        if self.field_names:
            lines.append(fmt(self.field_names))
            lines.append("-+-".join("-" * width for width in widths))
            for row in self._rows:
                lines.append(fmt(row))
        else:
            lines = [fmt(row) for row in self._rows]
        return "\n".join(lines)

    def __repr__(self):
        return str(self)
