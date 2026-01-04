/**
 * ENHANCED CONTENT BLOCK RENDERING
 * =================================
 *
 * This code snippet adds support for all academic content block types.
 * Insert these cases into the switch statement in renderContentBlock()
 * right before the 'derivation' case.
 */

            case 'note':
                // Academic note/aside - formatted as a highlighted box
                blockDiv.className = 'academic-note';
                blockDiv.innerHTML = `
                    <div class="note-content">${block.content || ''}</div>
                `;
                blockDiv.setAttribute('role', 'note');
                blockDiv.setAttribute('aria-label', 'Academic note');
                break;

            case 'highlight_box':
                // Highlighted information box
                blockDiv.className = 'highlight-box';
                blockDiv.innerHTML = `
                    ${block.title ? `<div class="highlight-title">${block.title}</div>` : ''}
                    <div class="highlight-content">${block.content || ''}</div>
                `;
                blockDiv.setAttribute('role', 'complementary');
                blockDiv.setAttribute('aria-label', 'Highlighted information');
                break;

            case 'definition':
                // Mathematical definition block
                blockDiv.className = 'definition-block';
                blockDiv.innerHTML = `
                    ${block.term ? `<div class="definition-term"><strong>Definition:</strong> ${block.term}</div>` : ''}
                    <div class="definition-content">${block.content || ''}</div>
                `;
                blockDiv.setAttribute('role', 'definition');
                break;

            case 'theorem':
                // Theorem block with optional proof
                blockDiv.className = 'theorem-block';
                blockDiv.innerHTML = `
                    <div class="theorem-header">
                        <span class="theorem-label">${block.label || 'Theorem'}</span>
                        ${block.title ? `<span class="theorem-title">${block.title}</span>` : ''}
                    </div>
                    <div class="theorem-content">${block.content || ''}</div>
                `;
                blockDiv.setAttribute('role', 'article');
                blockDiv.setAttribute('aria-label', 'Mathematical theorem');
                break;

            case 'proof':
                // Proof block
                blockDiv.className = 'proof-block';
                blockDiv.innerHTML = `
                    <div class="proof-header">Proof.</div>
                    <div class="proof-content">${block.content || ''}</div>
                    <div class="proof-end">∎</div>
                `;
                blockDiv.setAttribute('role', 'article');
                blockDiv.setAttribute('aria-label', 'Mathematical proof');
                break;

            case 'remark':
                // Remark/observation block
                blockDiv.className = 'remark-block';
                blockDiv.innerHTML = `
                    <div class="remark-header">${block.title || 'Remark'}</div>
                    <div class="remark-content">${block.content || ''}</div>
                `;
                blockDiv.setAttribute('role', 'note');
                break;

            case 'example':
                // Worked example block
                blockDiv.className = 'example-block';
                blockDiv.innerHTML = `
                    <div class="example-header">${block.title || 'Example'}</div>
                    <div class="example-content">${block.content || ''}</div>
                `;
                blockDiv.setAttribute('role', 'article');
                blockDiv.setAttribute('aria-label', 'Worked example');
                break;

/**
 * ACCESSIBILITY ENHANCEMENTS
 * ==========================
 *
 * Add these attributes to existing block types for better screen reader support:
 */

// For paragraph blocks - add after blockDiv.innerHTML line:
                blockDiv.setAttribute('role', 'article');

// For heading blocks - add after blockDiv.innerHTML line:
                if (block.label) {
                    blockDiv.id = block.label;
                }

// For formula/equation blocks - add role and aria-label to fallback:
                role="math" aria-label="Mathematical equation"

// For list blocks - add after blockDiv.innerHTML line:
                blockDiv.setAttribute('role', 'list');

// For code blocks - update pre tag:
                <pre role="code"><code...

// For quote blocks - update blockquote:
                <blockquote role="complementary">...

// For table blocks - add after renderTable call:
                blockDiv.setAttribute('role', 'table');

// At end of switch default case - add warning:
                console.warn(`PMPaperRenderer: Unknown block type: ${block.type}`);
