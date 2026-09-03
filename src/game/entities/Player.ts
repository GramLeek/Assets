import Phaser from 'phaser';

export class Player extends Phaser.Physics.Arcade.Sprite {
  private readonly cursors: Phaser.Types.Input.Keyboard.CursorKeys;
  private readonly wasd: Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>;
  readonly speed = 255;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'player');
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.setCollideWorldBounds(true);
    this.setDepth(20);

    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setCircle(17, 7, 7);

    const keyboard = scene.input.keyboard;
    if (!keyboard) throw new Error('Keyboard input unavailable');
    this.cursors = keyboard.createCursorKeys();
    this.wasd = keyboard.addKeys('W,A,S,D') as Record<'W' | 'A' | 'S' | 'D', Phaser.Input.Keyboard.Key>;
  }

  update(pointer: Phaser.Input.Pointer): void {
    let x = 0;
    let y = 0;
    if (this.cursors.left.isDown || this.wasd.A.isDown) x -= 1;
    if (this.cursors.right.isDown || this.wasd.D.isDown) x += 1;
    if (this.cursors.up.isDown || this.wasd.W.isDown) y -= 1;
    if (this.cursors.down.isDown || this.wasd.S.isDown) y += 1;

    const direction = new Phaser.Math.Vector2(x, y);
    if (direction.lengthSq() > 0) direction.normalize().scale(this.speed);
    this.setVelocity(direction.x, direction.y);

    const worldPoint = pointer.positionToCamera(this.scene.cameras.main) as Phaser.Math.Vector2;
    this.setRotation(Phaser.Math.Angle.Between(this.x, this.y, worldPoint.x, worldPoint.y) + Math.PI / 2);
  }
}
