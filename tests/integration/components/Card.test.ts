import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test } from 'vitest';
import Card from '../../../src/components/ui/Card.astro';

test('Card renders with default props', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card);

  expect(result).toContain('bg-white');
  expect(result).toContain('p-6'); // default padding is md
});

test('Card renders with custom props', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    props: { variant: 'elevated', padding: 'lg' },
  });

  expect(result).toContain('shadow-lg');
  expect(result).toContain('p-8');
});
