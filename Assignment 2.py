
        if name not in cls._templates:
            raise ValueError(f"Template '{name}' is not registered")

        report = cls(title, author)

        for sec_title in cls._templates[name]:
            report.add_section(sec_title, "<content pending>")

        return report

    @classmethod
    def available_templates(cls):
        return list(cls._templates.keys())

    # -----------------------------------------------------------------
    # INSTANCE METHODS
    # -----------------------------------------------------------------
    def add_section(self, title, content):
        self.sections.append(ReportSection(title, content))
        return self

    def set_content(self, title, content):
        """Fill in content for an existing (template-generated) section."""
        for sec in self.sections:
            if sec.title == title:
                sec.content = content
                return True
        return False

    @log_call
    @add_border("=", 50)
    def summary(self):
        """A short, decorator-formatted summary of the report."""
        return (f"Report: {self.title}\n"
                f"Author: {self.author}\n"
                f"Sections: {len(self.sections)}\n"
                f"Generated: {self.created_on:%Y-%m-%d %H:%M}")

    @bold
    def title_line(self):
        return self.title

    # -----------------------------------------------------------------
    # MAGIC METHODS
    # -----------------------------------------------------------------
    def __str__(self):
        lines = [f"REPORT: {self.title}", f"Author: {self.author}", "-" * 40]
        for sec in self.sections:
            lines.append(str(sec))
            lines.append("")
        return "\n".join(lines)

    def __repr__(self):
        return f"Report(title={self.title!r}, author={self.author!r}, sections={len(self.sections)})"

    def __len__(self):
        return len(self.sections)

    def __getitem__(self, index):
        return self.sections[index]

    def __iter__(self):
        return iter(self.sections)

    def __contains__(self, title):
        return any(sec.title == title for sec in self.sections)

    def __add__(self, other):
        if not isinstance(other, Report):
            return NotImplemented
        merged = Report(f"{self.title} & {other.title}", self.author)
        merged.sections = self.sections + other.sections
        return merged

    def __eq__(self, other):
        return (isinstance(other, Report)
                and self.title == other.title
                and self.sections == other.sections)

    def __call__(self, formatter=None):
        """Makes a Report object callable."""
        text = str(self)
        return formatter(text) if formatter else text


# =====================================================================
# 4. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    # Step A: Register templates dynamically
    Report.register_template(
        "project_report",
        ["Introduction", "Methodology", "Results", "Conclusion"]
    )

    Report.register_template(
        "attendance_report",
        ["Summary", "Defaulter List"]
    )

    print("\nAvailable templates:", Report.available_templates())

    # Step B: Build a report from a template
    r1 = Report.from_template(
        "project_report",
        "AI Lab Mini Project",
        author="DrVinodpuri"
    )

    r1.set_content("Introduction", "This project explores dynamic report generation.")
    r1.set_content("Methodology", "Used decorators, classmethods and magic methods.")
    r1.set_content("Results", "Report generated and formatted successfully.")
    r1.set_content("Conclusion", "OOP features simplify dynamic formatting.")

    # Step C: Build a second manually-created report
    r2 = Report("Attendance Snapshot", author="Rahul")
    r2.add_section("Summary", "92% average attendance this month.")

    # Step D: Use magic methods
    print("\n--- len(r1) ---")
    print(len(r1))

    print("\n--- r1[0] ---")
    print(r1[0])

    print("\n--- iterate over r1 ---")
    for section in r1:
        print(" •", section.title)

    print("\n--- 'Results' in r1 ---")
    print("Results" in r1)

    print("\n--- combine r1 + r2 ---")
    combined = r1 + r2
    print(combined)

    # Step E: Apply formatting decorators dynamically
    print("\n--- decorated summary() [bordered + logged] ---")
    print(r1.summary())

    print("\n--- title_line() [bold] ---")
    print(r1.title_line())

    print("\n--- report as callable, formatted UPPERCASE on the fly ---")
    print(r1(formatter=str.upper))

    print("\n--- report as callable, default (no formatter) ---")
    print(r2())
