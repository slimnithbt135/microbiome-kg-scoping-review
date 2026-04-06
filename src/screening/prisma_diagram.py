import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

def box(x, y, w, h, text):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.02",
                               edgecolor='black',
                               facecolor='white',
                               linewidth=1.5))
    ax.text(x + w/2, y + h/2, text,
            ha='center', va='center', fontsize=9)

# Boxes
box(2, 12, 6, 1.2, "Records identified\n(n = 796)")
box(2, 10.5, 6, 1.2, "After duplicates removed\n(n = 769)")
box(2, 9, 6, 1.2, "Records screened\n(n = 769)")
box(2, 7.5, 6, 1.2, "Records excluded\n(n = 715)")
box(2, 6, 6, 1.2, "Full-text assessed\n(n = 54)")
box(2, 4.5, 6, 1.2, "Studies included\n(n = 54)")

# Arrows
for y in [11.2, 9.7, 8.2, 6.7, 5.2]:
    ax.annotate('', xy=(5, y), xytext=(5, y+0.8),
                arrowprops=dict(arrowstyle='->', lw=1.5))

plt.savefig("PRISMA_diagram.png", dpi=600, bbox_inches='tight')
plt.savefig("PRISMA_diagram.pdf", bbox_inches='tight')
plt.show()
