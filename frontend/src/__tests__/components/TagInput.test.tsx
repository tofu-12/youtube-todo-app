import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TagInput from "@/components/TagInput";
import type { TagOut } from "@/lib/types";

const mockGetTags = vi.fn().mockResolvedValue([
  { id: "t1", name: "chest" },
  { id: "t2", name: "back" },
  { id: "t3", name: "arms" },
]);
vi.mock("@/lib/api", () => ({
  getTags: (...args: unknown[]) => mockGetTags(...args),
}));

beforeEach(() => {
  vi.clearAllMocks();
  mockGetTags.mockResolvedValue([
    { id: "t1", name: "chest" },
    { id: "t2", name: "back" },
    { id: "t3", name: "arms" },
  ]);
});

describe("TagInput", () => {
  it("renders selected tags as pills", () => {
    const tags: TagOut[] = [
      { id: "t1", name: "chest" },
      { id: "t2", name: "back" },
    ];
    render(<TagInput selectedTags={tags} onChange={vi.fn()} />);

    expect(screen.getByText("chest")).toBeInTheDocument();
    expect(screen.getByText("back")).toBeInTheDocument();
  });

  it("filters suggestions by input", async () => {
    const user = userEvent.setup();
    render(<TagInput selectedTags={[]} onChange={vi.fn()} />);

    const input = screen.getByLabelText("タグ入力");
    await user.type(input, "ch");

    await waitFor(() => {
      expect(screen.getByText("chest")).toBeInTheDocument();
    });
    expect(screen.queryByText("back")).not.toBeInTheDocument();
  });

  it("adds tag when suggestion is clicked", async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();
    render(<TagInput selectedTags={[]} onChange={onChange} />);

    const input = screen.getByLabelText("タグ入力");
    await user.type(input, "ch");

    await waitFor(() => {
      expect(screen.getByText("chest")).toBeInTheDocument();
    });
    await user.click(screen.getByText("chest"));

    expect(onChange).toHaveBeenCalledWith([{ id: "t1", name: "chest" }]);
  });

  it("removes tag when × is clicked", async () => {
    const onChange = vi.fn();
    const tags: TagOut[] = [{ id: "t1", name: "chest" }];
    const user = userEvent.setup();
    render(<TagInput selectedTags={tags} onChange={onChange} />);

    await user.click(screen.getByLabelText("chestを削除"));

    expect(onChange).toHaveBeenCalledWith([]);
  });

  it("shows create option for new tag", async () => {
    const user = userEvent.setup();
    render(<TagInput selectedTags={[]} onChange={vi.fn()} />);

    const input = screen.getByLabelText("タグ入力");
    await user.type(input, "legs");

    await waitFor(() => {
      expect(screen.getByText("「legs」を新規作成")).toBeInTheDocument();
    });
  });

  it("adds new tag via create option", async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();
    render(<TagInput selectedTags={[]} onChange={onChange} />);

    const input = screen.getByLabelText("タグ入力");
    await user.type(input, "legs");

    await waitFor(() => {
      expect(screen.getByText("「legs」を新規作成")).toBeInTheDocument();
    });
    await user.click(screen.getByText("「legs」を新規作成"));

    expect(onChange).toHaveBeenCalledWith([{ id: "", name: "legs" }]);
  });

  it("does not show already selected tags in suggestions", async () => {
    const user = userEvent.setup();
    const tags: TagOut[] = [{ id: "t1", name: "chest" }];
    render(<TagInput selectedTags={tags} onChange={vi.fn()} />);

    const input = screen.getByLabelText("タグ入力");
    await user.type(input, "c");

    await waitFor(() => {
      // "chest" should not appear in suggestions since it's already selected
      const listItems = screen.queryAllByRole("listitem");
      const chestItems = listItems.filter((el) => el.textContent === "chest");
      expect(chestItems).toHaveLength(0);
    });
  });
});
